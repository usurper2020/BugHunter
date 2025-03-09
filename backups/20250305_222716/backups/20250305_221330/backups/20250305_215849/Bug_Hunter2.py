import asyncio
import logging
import os
import sys
import time
import traceback
from pathlib import Path
from typing import List, Dict, Any
import black
import isort
import autopep8
import ast
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tqdm import tqdm


class OptimizedBugHunterFixer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.stats = {
            "start_time": time.time(),
            "success_files": set(),
            "error_files": set(),
            "memory_usage": [],
            "cpu_usage": [],
        }
        self.processed_files = set()
        self._processed_count = 0
        self.excluded_folders = {
            "__pycache__",
            "venv",
            ".git",
            "node_modules",
            "backups",
        }

        # Initialize backup directory
        self.backup_dir = self.project_dir / \
            "backups" / time.strftime("%Y%m%d_%H%M%S")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Configure process pools
        self.max_workers = os.cpu_count() or 4
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers * 2)

        logging.info(f"Starting Bug Hunter in directory: {project_dir}")

    async def process_files_async(self, files: List[Path]) -> None:
        """Process files asynchronously with enhanced error handling."""
        total_files = len(files)
        processed_files = 0
        chunk_size = min(100, max(10, self.max_workers * 2))

        with tqdm(total=total_files, desc="Processing files") as pbar:
            for i in range(0, total_files, chunk_size):
                chunk = files[i: i + chunk_size]
                tasks = []

                for file_path in chunk:
                    if self.is_valid_python_file(file_path):
                        tasks.append(self._async_process_file(file_path))

                if not tasks:
                    continue

                try:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    processed = len(
                        [
                            r
                            for r in results
                            if isinstance(r, dict) and r.get("status") == "success"
                        ]
                    )
                    processed_files += processed
                    pbar.update(len(chunk))
                except Exception as e:
                    logging.error(f"Chunk processing error: {e}")
                    continue

    async def _async_process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file asynchronously with improved error handling."""
        try:
            if not file_path.exists():
                return {
                    "file": file_path,
                    "status": "error",
                    "error": "File does not exist",
                }

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, "r", encoding="latin-1") as f:
                        content = f.read()
                except Exception as e:
                    return {
                        "file": file_path,
                        "status": "error",
                        "error": f"File reading error: {str(e)}",
                    }

            # Create backup
            await self.backup_file_async(file_path)

            # Apply formatting
            try:
                formatted = await self.format_content_async(content)

                if formatted != content:
                    try:
                        ast.parse(formatted)  # Validate syntax
                        async with asyncio.Lock():
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(formatted)
                        return {"file": file_path, "status": "success"}
                    except SyntaxError as e:
                        return {
                            "file": file_path,
                            "status": "error",
                            "error": f"Invalid formatted content: {str(e)}",
                        }
                return {
                    "file": file_path,
                    "status": "success",
                    "message": "No changes needed",
                }

            except Exception as e:
                return {
                    "file": file_path,
                    "status": "error",
                    "error": f"Formatting error: {str(e)}",
                }

        except Exception as e:
            return {"file": file_path, "status": "error", "error": str(e)}

    async def backup_file_async(self, file_path: Path) -> None:
        """Create backup of file asynchronously."""
        try:
            relative_path = file_path.relative_to(self.project_dir)
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            async with asyncio.Lock():
                with open(file_path, "r", encoding="utf-8") as source:
                    content = source.read()
                with open(backup_path, "w", encoding="utf-8") as target:
                    target.write(content)
        except Exception as e:
            logging.error(f"Backup failed for {file_path}: {e}")

    async def format_content_async(self, content: str) -> str:
        """Format content asynchronously using multiple formatters."""
        try:
            # Apply black
            try:
                content = black.format_str(content, mode=black.FileMode())
            except Exception as e:
                logging.warning(f"Black formatting failed: {e}")

            # Apply isort
            try:
                content = isort.code(content)
            except Exception as e:
                logging.warning(f"Isort formatting failed: {e}")

            # Apply autopep8
            try:
                content = autopep8.fix_code(content)
            except Exception as e:
                logging.warning(f"Autopep8 formatting failed: {e}")

            return content
        except Exception as e:
            logging.error(f"Formatting failed: {e}")
            return content

    def is_valid_python_file(self, file_path: Path) -> bool:
        """Check if file is a valid Python file and should be processed."""
        try:
            if not file_path.is_file() or file_path.suffix != ".py":
                return False

            if any(excluded in file_path.parts for excluded in self.excluded_folders):
                return False

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    ast.parse(content)
                    return True
            except (SyntaxError, UnicodeDecodeError):
                return False

        except Exception as e:
            logging.debug(f"Invalid Python file {file_path}: {e}")
            return False


if __name__ == "__main__":
    try:
        # Initialize the bug hunter
        print(f"Initializing Bug Hunter for directory: .\\")
        hunter = OptimizedBugHunterFixer(".")

        # Get list of Python files
        python_files = list(Path(".").rglob("*.py"))
        print(f"Found {len(python_files)} Python files to process")

        # Process files asynchronously
        print("Starting file processing...")
        asyncio.run(hunter.process_files_async(python_files))

        print("\nProcessing complete!")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)
