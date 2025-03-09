import asyncio
import logging
import os
import sys
import time
import traceback
from pathlib import Path
from typing import List, Dict, Any, Set
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import black
import isort
import autopep8
import ast
from tqdm import tqdm
import multiprocessing
import threading
import functools
import itertools
from collections import deque
import cachetools
import xxhash
import psutil


class BugHunter:
    def __init__(self, project_dir: str):
        """Initialize BugHunter with optimized settings."""
        self.project_dir = Path(project_dir)
        self.start_time = time.time()

        # Statistics tracking
        self.stats = {"processed": 0, "success": 0, "errors": 0, "skipped": 0}

        # System optimization
        self.cpu_count = multiprocessing.cpu_count()
        self.chunk_size = max(250, self.cpu_count * 8)
        self.max_threads = self.cpu_count * 4
        self.max_processes = self.cpu_count

        # Thread safety
        self.stats_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.stop_event = threading.Event()

        # Processing queues
        self.file_queue = deque()
        self.result_queue = deque()

        # Initialize thread and process pools
        self.thread_pool = ThreadPoolExecutor(
            max_workers=self.max_threads, thread_name_prefix="BugHunter"
        )
        self.process_pool = ProcessPoolExecutor(
            max_workers=self.max_processes,
            mp_context=multiprocessing.get_context("spawn"),
        )

        # Caching
        self._validation_cache = cachetools.LRUCache(maxsize=50000)

        # File patterns
        import re

        self.excluded_patterns = re.compile(
            r"(__pycache__|venv|\.env|node_modules|\.git|\.idea|\.vscode|build|dist)"
        )

        # Formatter configurations
        self.black_mode = black.FileMode()
        self.isort_config = {
            "profile": "black",
            "multi_line_output": 3,
            "lines_after_imports": 2,
            "include_trailing_comma": True,
            "force_grid_wrap": 0,
            "use_parentheses": True,
            "ensure_newline_before_comments": True,
        }

        # Setup backup directory
        self.backup_dir = self.setup_backup_dir()

        # Track processed files
        self.processed_files: Set[Path] = set()

        # Batch processing
        self.batch_size = 1000

        # Windows-specific optimizations
        if sys.platform == "win32":
            self.process = psutil.Process()
            self.process.nice(psutil.HIGH_PRIORITY_CLASS)
            self.buffer_size = 65536
        else:
            os.nice(-10)
            self.buffer_size = -1

    def setup_backup_dir(self) -> Path:
        """Create and return backup directory path."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_dir = self.project_dir / "backups" / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    @functools.lru_cache(maxsize=1024)
    def get_file_hash(self, file_path: str) -> str:
        """Generate fast file hash."""
        return xxhash.xxh64(file_path).hexdigest()

    def is_valid_python_file(self, file_path: Path) -> bool:
        """Check if file is a valid Python file."""
        try:
            if not file_path.is_file() or file_path.suffix != ".py":
                return False

            if self.excluded_patterns.search(str(file_path)):
                return False

            file_hash = self.get_file_hash(str(file_path))
            if file_hash in self._validation_cache:
                return self._validation_cache[file_hash]

            with open(file_path, "rb") as f:
                ast.parse(f.read())
            self._validation_cache[file_hash] = True
            return True
        except Exception:
            self._validation_cache[file_hash] = False
            return False

    async def read_file_content(self, file_path: Path) -> str:
        """Read file content with proper encoding."""
        try:
            async with asyncio.Lock():
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                    buffering=self.buffer_size,
                ) as f:
                    return f.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            return ""

    async def write_changes(self, file_path: Path, content: str) -> bool:
        """Write changes to file."""
        try:
            async with asyncio.Lock():
                with open(
                    file_path, "w", encoding="utf-8", buffering=self.buffer_size
                ) as f:
                    f.write(content)
            return True
        except Exception as e:
            logging.error(f"Error writing to {file_path}: {e}")
            return False

    async def create_backup(self, file_path: Path, content: str) -> None:
        """Create file backup."""
        try:
            relative_path = file_path.relative_to(self.project_dir)
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            async with asyncio.Lock():
                with open(
                    backup_path, "w", encoding="utf-8", buffering=self.buffer_size
                ) as f:
                    f.write(content)
        except Exception as e:
            logging.error(f"Backup failed for {file_path}: {e}")

    async def format_content(self, content: str) -> str:
        """Format file content using multiple formatters."""
        try:
            content = black.format_str(content, mode=self.black_mode)
            content = isort.code(content, **self.isort_config)
            content = autopep8.fix_code(content)
            return content
        except Exception as e:
            logging.error(f"Formatting failed: {e}")
            return content

    async def process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Process individual file."""
        try:
            content = await self.read_file_content(file_path)
            if not content:
                return {"status": "error", "file": file_path, "error": "Read failed"}

            await self.create_backup(file_path, content)
            formatted_content = await self.format_content(content)

            if formatted_content != content:
                if await self.write_changes(file_path, formatted_content):
                    return {"status": "success", "file": file_path, "changes": True}
                return {"status": "error", "file": file_path, "error": "Write failed"}

            return {"status": "success", "file": file_path, "changes": False}
        except Exception as e:
            return {"status": "error", "file": file_path, "error": str(e)}

    async def process_files_parallel(self, files: List[Path]) -> None:
        """Process files in parallel."""
        pbar = None
        try:
            valid_files = [f for f in files if self.is_valid_python_file(f)]

            if not valid_files:
                logging.warning("No valid Python files found")
                return

            pbar = tqdm(
                total=len(valid_files),
                desc="Processing files",
                unit="files",
                miniters=1,
            )

            semaphore = asyncio.Semaphore(self.max_processes * 2)
            tasks = []

            for file_path in valid_files:
                if self.stop_event.is_set():
                    break

                async with semaphore:
                    task = asyncio.create_task(
                        self.process_single_file(file_path))
                    tasks.append(task)

                    def callback(task):
                        pbar.update(1)

                    task.add_done_callback(callback)

            results = await asyncio.gather(*tasks, return_exceptions=True)
            self.update_stats(results)

        except Exception as e:
            logging.error(f"Parallel processing error: {e}")
        finally:
            if pbar:
                pbar.close()
            await self.cleanup()

    def update_stats(self, results: List[Dict[str, Any]]) -> None:
        """Update processing statistics."""
        with self.stats_lock:
            for result in results:
                if isinstance(result, dict):
                    self.stats["processed"] += 1
                    if result["status"] == "success":
                        self.stats["success"] += 1
                    else:
                        self.stats["errors"] += 1

    async def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            self.thread_pool.shutdown(wait=False)
            self.process_pool.shutdown(wait=False)
            self._validation_cache.clear()
            await self.generate_report()
        except Exception as e:
            logging.error(f"Cleanup error: {e}")

    async def generate_report(self) -> None:
        """Generate processing report."""
        try:
            report_path = self.project_dir / "bug_hunter_report.txt"
            async with asyncio.Lock():
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write("Bug Hunter Processing Report\n")
                    f.write("==========================\n\n")
                    f.write(
                        f"Total files processed: {self.stats['processed']}\n")
                    f.write(
                        f"Successfully processed: {self.stats['success']}\n")
                    f.write(f"Errors encountered: {self.stats['errors']}\n")
                    f.write(f"Files skipped: {self.stats['skipped']}\n")
                    f.write(
                        f"Total processing time: {time.time() - self.start_time:.2f}s\n"
                    )
        except Exception as e:
            logging.error(f"Report generation failed: {e}")


def main():
    """Main execution function."""
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    "bug_hunter.log", mode="w", encoding="utf-8"),
            ],
        )

        print("Initializing Bug Hunter...")
        hunter = BugHunter(".")

        python_files = list(Path(".").rglob("*.py"))
        total_files = len(python_files)
        print(f"Found {total_files} Python files to process")

        if total_files == 0:
            print("No Python files found to process.")
            return

        print("Starting file processing...")
        asyncio.run(hunter.process_files_parallel(python_files))

        print("\nProcessing complete! Check bug_hunter_report.txt for details.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
