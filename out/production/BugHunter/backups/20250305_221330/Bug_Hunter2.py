import ast
import asyncio
import logging
import multiprocessing
import os
import queue
import signal
import sys
import threading
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Set

import autopep8
import black
import isort
from tqdm import tqdm


class OptimizedBugHunterFixer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.start_time = time.time()
        self.stats = {"processed": 0, "success": 0, "errors": 0, "skipped": 0}

        # Performance optimization settings
        self.cpu_count = multiprocessing.cpu_count()
        self.chunk_size = max(100, self.cpu_count * 4)
        self.max_threads = self.cpu_count * 2
        self.max_processes = self.cpu_count

        # Thread-safe queues
        self.file_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # Locks and events
        self.stats_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.stop_event = threading.Event()

        # Initialize pools
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_threads)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_processes)

        # Validation cache
        self._validation_cache = {}

        # Initialize backup directory
        self.backup_dir = self.setup_backup_dir()

        # Set of processed files for deduplication
        self.processed_files: Set[Path] = set()

        # Signal handling
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def setup_backup_dir(self) -> Path:
        """Setup backup directory with timestamp."""
        backup_dir = self.project_dir / "backups" / \
            time.strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def handle_interrupt(self, signum, frame):
        """Handle interrupt signal gracefully."""
        logging.info("Received interrupt signal. Cleaning up...")
        self.stop_event.set()
        self.cleanup()
        sys.exit(0)

    async def process_files_parallel(self, files: List[Path]) -> None:
        """Process files using both async and parallel processing."""
        pbar = None
        try:
            # Filter valid files first
            valid_files = [f for f in files if self.is_valid_python_file(f)]
            total_files = len(valid_files)

            if not total_files:
                logging.warning("No valid Python files found to process")
                return

            # Initialize progress bar
            pbar = tqdm(
                total=total_files,
                desc="Processing files",
                unit="files",
                ncols=80,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            )

            # Create chunks for parallel processing
            chunks = [
                valid_files[i: i + self.chunk_size]
                for i in range(0, len(valid_files), self.chunk_size)
            ]

            # Process chunks in parallel
            tasks = []
            for chunk in chunks:
                if self.stop_event.is_set():
                    break
                tasks.append(self.process_chunk(chunk, pbar))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            logging.error(f"Parallel processing error: {e}")
        finally:
            if pbar is not None:
                pbar.close()
            self.cleanup()

    async def process_chunk(self, chunk: List[Path], pbar: tqdm) -> None:
        """Process a chunk of files using thread pool."""
        try:
            # Create tasks for each file in the chunk
            tasks = []
            for file_path in chunk:
                if self.stop_event.is_set():
                    break
                if file_path not in self.processed_files:
                    tasks.append(self.process_single_file(file_path))
                    self.processed_files.add(file_path)

            # Process tasks concurrently
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Update progress and stats
                with self.stats_lock:
                    for result in results:
                        if isinstance(result, dict):
                            self.update_stats(result)
                            pbar.update(1)

        except Exception as e:
            logging.error(f"Chunk processing error: {e}")

    async def process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file with optimized error handling."""
        try:
            # Read file content
            content = await self.read_file_content(file_path)
            if not content:
                return {
                    "status": "error",
                    "file": file_path,
                    "error": "Failed to read file",
                }

            # Create backup
            await self.create_backup(file_path, content)

            # Format content
            formatted_content = await self.format_content(content)
            if not formatted_content:
                return {
                    "status": "error",
                    "file": file_path,
                    "error": "Formatting failed",
                }

            # Write changes if needed
            if formatted_content != content:
                success = await self.write_changes(file_path, formatted_content)
                if success:
                    return {"status": "success", "file": file_path, "changes": True}
                return {
                    "status": "error",
                    "file": file_path,
                    "error": "Failed to write changes",
                }

            return {"status": "success", "file": file_path, "changes": False}

        except Exception as e:
            return {"status": "error", "file": file_path, "error": str(e)}

    async def read_file_content(self, file_path: Path) -> str:
        """Read file content with multiple encoding attempts."""
        encodings = ["utf-8", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                async with asyncio.Lock():
                    with open(file_path, "r", encoding=encoding) as f:
                        return f.read()
            except Exception:
                continue
        return ""

    async def create_backup(self, file_path: Path, content: str) -> None:
        """Create backup of file content."""
        try:
            relative_path = file_path.relative_to(self.project_dir)
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            async with asyncio.Lock():
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception as e:
            logging.error(f"Backup failed for {file_path}: {e}")

    async def format_content(self, content: str) -> str:
        """Format content using multiple formatters."""
        try:
            # Apply black formatting
            content = black.format_str(content, mode=black.FileMode())

            # Apply isort
            content = isort.code(content)

            # Apply autopep8
            content = autopep8.fix_code(content)

            return content
        except Exception as e:
            logging.error(f"Formatting failed: {e}")
            return content

    async def write_changes(self, file_path: Path, content: str) -> bool:
        """Write changes to file with validation."""
        try:
            # Validate syntax before writing
            ast.parse(content)

            async with asyncio.Lock():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            return True

        except Exception as e:
            logging.error(f"Failed to write changes to {file_path}: {e}")
            return False

    def is_valid_python_file(self, file_path: Path) -> bool:
        """Efficiently validate Python files with caching."""
        try:
            # Quick checks first
            if not file_path.is_file() or file_path.suffix != ".py":
                return False

            # Check excluded patterns
            excluded_patterns = {
                "__pycache__",
                "venv",
                ".env",
                "node_modules",
                ".git",
                ".idea",
                ".vscode",
                "build",
                "dist",
            }
            if any(pattern in str(file_path) for pattern in excluded_patterns):
                return False

            # Cache check
            file_hash = hash(str(file_path))
            if file_hash in self._validation_cache:
                return self._validation_cache[file_hash]

            # Validate syntax
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
                self._validation_cache[file_hash] = True
                return True
            except (SyntaxError, UnicodeDecodeError):
                self._validation_cache[file_hash] = False
                return False

        except Exception as e:
            logging.debug(f"File validation error for {file_path}: {e}")
            return False

    def update_stats(self, result: Dict[str, Any]) -> None:
        """Update processing statistics."""
        with self.stats_lock:
            self.stats["processed"] += 1
            if result["status"] == "success":
                self.stats["success"] += 1
            elif result["status"] == "error":
                self.stats["errors"] += 1

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.thread_pool.shutdown(wait=False)
        self.process_pool.shutdown(wait=False)
        self.generate_report()

    def generate_report(self) -> None:
        """Generate processing report."""
        try:
            report_path = self.project_dir / "bug_hunter_report.txt"
            with open(report_path, "w") as f:
                f.write("Bug Hunter Processing Report\n")
                f.write("==========================\n\n")
                f.write(f"Total files processed: {self.stats['processed']}\n")
                f.write(f"Successfully processed: {self.stats['success']}\n")
                f.write(f"Errors encountered: {self.stats['errors']}\n")
                f.write(f"Files skipped: {self.stats['skipped']}\n")
                f.write(
                    f"Total processing time: {time.time() - self.start_time:.2f}s\n"
                )
        except Exception as e:
            logging.error(f"Failed to generate report: {e}")


if __name__ == "__main__":
    try:
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(
            ), logging.FileHandler("bug_hunter.log")],
        )

        print("Initializing Bug Hunter...")
        hunter = OptimizedBugHunterFixer(".")

        # Get Python files
        python_files = list(Path(".").rglob("*.py"))
        total_files = len(python_files)
        print(f"Found {total_files} Python files to process")

        if total_files == 0:
            print("No Python files found to process.")
            sys.exit(0)

        # Process files
        print("Starting file processing...")
        asyncio.run(hunter.process_files_parallel(python_files))

        print("\nProcessing complete! Check bug_hunter_report.txt for analysis.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)
