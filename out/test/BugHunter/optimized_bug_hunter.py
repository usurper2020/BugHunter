#!/usr/bin/env python3
"""
Optimized Bug Hunter & Code Fixer - Complete Updated Version
Advanced Python code analysis and fixing tool with enhanced error handling
"""

import ast
import asyncio
import concurrent.futures
import gc
import hashlib
import logging
import mmap
import multiprocessing
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import tokenize
import traceback
import zlib
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from functools import lru_cache
from pathlib import Path
from queue import Queue
from typing import (Any, Dict, Generator, List, Optional, Set, Tuple, TypeVar,
                    Union)

try:
    import autopep8
    import black
    import isort
    import numpy as np
    import psutil
    import pylint.lint
    from tqdm import tqdm
except ImportError as e:
    print(f"Error: Required package not found. Please install required packages: {e}")
    print("Run: pip install autopep8 black isort tqdm pylint psutil numpy")
    sys.exit(1)

T = TypeVar("T")


class OptimizedBugHunterFixer:
    """Advanced Python code analysis and fixing tool with enhanced error handling."""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.backup_dir = self.project_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Performance optimization
        self.max_workers = min(32, multiprocessing.cpu_count() * 2)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers * 2)

        # Queue management
        self.file_queue = Queue()
        self.results_queue = Queue()
        self.error_queue = Queue()

        # Performance tracking
        self.performance_metrics = {}
        self.pylint_scores = {}

        # Memory management
        self.memory_threshold = 0.85
        self.current_memory_usage = 0.0
        self.memory_check_interval = 5

        # Batch processing
        self.batch_size = min(100, max(10, self.max_workers * 10))
        self.current_batch = []

        # Statistics
        self.stats = {
            "files_processed": 0,
            "errors_fixed": 0,
            "syntax_errors": 0,
            "import_errors": 0,
            "indentation_errors": 0,
            "start_time": time.time(),
            "processing_times": [],
            "memory_usage": [],
            "cpu_usage": [],
            "error_files": set(),
            "success_files": set(),
        }

        # Thread safety
        self._lock = threading.Lock()
        self._processed_count = 0
        self._error_count = 0

        # Optimization flags
        self.use_mmap = True
        self.use_compression = True
        self.cache_enabled = True

        # Excluded paths
        self.excluded_folders = {
            ".venv",
            "venv",
            "env",
            ".env",
            ".git",
            ".idea",
            ".vscode",
            "__pycache__",
            "build",
            "dist",
            "migrations",
            "node_modules",
            "test",
            "tests",
            "tmp",
            "temp",
            "logs",
            "log",
            "cache",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "htmlcov",
        }

        # Initialize systems
        self.setup_logging()
        self.setup_optimized_environment()
        self.initialize_caches()
        self.create_backup_directory()

    def setup_logging(self) -> None:
        """Configure enhanced logging system with rotation and formatting."""
        log_dir = self.project_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f'bug_hunter_{time.strftime("%Y%m%d_%H%M%S")}.log'

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
        )
        logging.info(f"Starting Bug Hunter in directory: {self.project_dir}")

    def setup_optimized_environment(self) -> None:
        """Configure environment for optimal performance."""
        try:
            # Set process priority
            process = psutil.Process(os.getpid())
            if hasattr(process, "nice"):
                process.nice(10)  # Lower priority to avoid system overload

            # Configure garbage collection
            gc.enable()
            gc.set_threshold(700, 10, 5)

            # Start performance monitoring
            self.start_performance_monitoring()

            logging.info("Environment optimization complete")
        except Exception as e:
            logging.error(f"Environment setup error: {e}")

    def start_performance_monitoring(self) -> None:
        """Initialize performance monitoring systems."""

        def monitor_resources():
            while True:
                try:
                    process = psutil.Process()
                    self.current_memory_usage = process.memory_percent()

                    if self.current_memory_usage > self.memory_threshold:
                        self.handle_high_memory_usage()

                    self.stats["memory_usage"].append(self.current_memory_usage)
                    self.stats["cpu_usage"].append(process.cpu_percent())

                    time.sleep(self.memory_check_interval)
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                    break

        threading.Thread(target=monitor_resources, daemon=True).start()

    def handle_high_memory_usage(self) -> None:
        """Handle high memory usage situations."""
        logging.warning("High memory usage detected. Initiating cleanup...")

        # Clear caches
        if self.cache_enabled:
            self.file_content_cache.clear()
            self.syntax_tree_cache.clear()
            self.pylint_cache.clear()
            self.format_cache.clear()

        # Force garbage collection
        gc.collect()

        # Pause processing if necessary
        if self.current_memory_usage > 0.95:  # 95% memory usage
            logging.warning("Critical memory usage. Pausing processing...")
            time.sleep(5)  # Wait for memory to be freed

    def initialize_caches(self) -> None:
        """Initialize enhanced caching system."""
        self.file_content_cache = {}
        self.syntax_tree_cache = {}
        self.pylint_cache = {}
        self.format_cache = {}
        self.error_cache = {}

    def create_backup_directory(self) -> None:
        """Create timestamped backup directory."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.current_backup_dir = self.backup_dir / timestamp
        self.current_backup_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created backup directory: {self.current_backup_dir}")

    def backup_file(self, file_path: Path) -> None:
        """Create backup of file before modification."""
        try:
            relative_path = file_path.relative_to(self.project_dir)
            backup_path = self.current_backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil

            shutil.copy2(file_path, backup_path)
            logging.debug(f"Created backup: {backup_path}")
        except Exception as e:
            logging.error(f"Backup failed for {file_path}: {e}")


def is_valid_python_file(self, file_path: Path) -> bool:
    """Check if file is a valid Python file and should be processed."""
    try:
        if not file_path.is_file() or file_path.suffix != ".py":
            return False

        # Check if file is in excluded directory
        for excluded in self.excluded_folders:
            if excluded in file_path.parts:
                return False

        # Try to read and parse file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                ast.parse(content)
                return True
        except (SyntaxError, UnicodeDecodeError):
            # Try with different encoding
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()
                    ast.parse(content)
                    return True
            except:
                return False

    except Exception as e:
        logging.debug(f"Invalid Python file {file_path}: {e}")
        return False

    async def process_files_async(self, files: List[Path]) -> None:
        """Process files asynchronously with enhanced error handling."""
        total_files = len(files)
        processed_files = 0
        chunk_size = min(100, max(10, self.max_workers * 2))

        with tqdm(total=total_files, desc="Processing files") as pbar:
            # Process files in chunks
            for i in range(0, total_files, chunk_size):
                chunk = files[i : i + chunk_size]
                tasks = []

                # Create tasks for chunk
                for file_path in chunk:
                    if self.is_valid_python_file(file_path):
                        tasks.append(self._async_process_file(file_path))

                if not tasks:
                    continue

                try:
                    # Process chunk of files
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # Handle results
                    self._handle_chunk_results(results)

                    # Update progress
                    processed = len(
                        [
                            r
                            for r in results
                            if isinstance(r, dict) and r.get("status") == "success"
                        ]
                    )
                    self._update_progress(processed, pbar)

                except Exception as e:
                    logging.error(f"Chunk processing error: {e}")
                    continue

                # Memory management
                if self.current_memory_usage > self.memory_threshold:
                    self.handle_high_memory_usage()


async def _async_process_file(self, file_path: Path) -> Dict[str, Any]:
    """Process a single file asynchronously with improved error handling."""
    try:
        # First check if file exists and is readable
        if not file_path.exists():
            return {
                "file": file_path,
                "status": "error",
                "error": "File does not exist",
            }

        # Read file content with explicit encoding handling
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                # Try alternative encoding
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()
            except Exception as e:
                return {
                    "file": file_path,
                    "status": "error",
                    "error": f"File reading error: {str(e)}",
                }

        # Create backup before modifications
        try:
            self.backup_file(file_path)
        except Exception as e:
            logging.warning(f"Backup creation failed for {file_path}: {e}")

        # Validate Python syntax before formatting
        try:
            ast.parse(content)
        except SyntaxError as e:
            return {
                "file": file_path,
                "status": "error",
                "error": f"Syntax error: {str(e)}",
            }

        # Apply formatting with individual try-except blocks
        try:
            # First try black
            try:
                formatted = black.format_file_contents(
                    content,
                    fast=False,
                    mode=black.FileMode(
                        line_length=88,
                        string_normalization=True,
                        is_pyi=file_path.suffix == ".pyi",
                    ),
                )
            except Exception as e:
                logging.warning(f"Black formatting failed for {file_path}: {e}")
                formatted = content

            # Then try isort
            try:
                formatted = isort.code(formatted)
            except Exception as e:
                logging.warning(f"Isort formatting failed for {file_path}: {e}")

            # Finally try autopep8
            try:
                formatted = autopep8.fix_code(formatted)
            except Exception as e:
                logging.warning(f"Autopep8 formatting failed for {file_path}: {e}")

            # Only write back if changes were made and content is valid
            if formatted != content:
                try:
                    # Validate the formatted content before writing
                    ast.parse(formatted)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(formatted)
                except (SyntaxError, Exception) as e:
                    return {
                        "file": file_path,
                        "status": "error",
                        "error": f"Invalid formatted content: {str(e)}",
                    }

            return {"file": file_path, "status": "success"}

        except Exception as e:
            return {
                "file": file_path,
                "status": "error",
                "error": f"Formatting error: {str(e)}",
            }

    except Exception as e:
        return {"file": file_path, "status": "error", "error": str(e)}

    def _handle_chunk_results(self, results: List[Dict[str, Any]]) -> None:
        """Handle results from processing a chunk of files."""
        for result in results:
            if result["status"] == "success":
                self.stats["success_files"].add(result["file"])
            else:
                self.stats["error_files"].add(result["file"])
                logging.error(
                    f"Error processing {result['file']}: {result.get('error')}"
                )

    def _update_progress(self, count: int, pbar: tqdm) -> None:
        """Update progress bar and statistics."""
        with self._lock:
            self._processed_count += count
            pbar.update(count)

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive processing report."""
        end_time = time.time()
        processing_time = end_time - self.stats["start_time"]

        report = {
            "total_files_processed": self._processed_count,
            "successful_files": len(self.stats["success_files"]),
            "failed_files": len(self.stats["error_files"]),
            "processing_time": processing_time,
            "average_memory_usage": np.mean(self.stats["memory_usage"])
            if self.stats["memory_usage"]
            else 0,
            "peak_memory_usage": max(self.stats["memory_usage"])
            if self.stats["memory_usage"]
            else 0,
            "average_cpu_usage": np.mean(self.stats["cpu_usage"])
            if self.stats["cpu_usage"]
            else 0,
        }

        # Save report to file
        report_path = self.project_dir / "bug_hunter_report.txt"
        with open(report_path, "w") as f:
            for key, value in report.items():
                f.write(f"{key}: {value}\n")

        return report

    def cleanup(self) -> None:
        """Perform cleanup operations."""
        try:
            # Close process pools
            self.process_pool.shutdown(wait=True)
            self.thread_pool.shutdown(wait=True)

            # Clear caches
            self.initialize_caches()

            # Force garbage collection
            gc.collect()

            logging.info("Cleanup completed successfully")
        except Exception as e:
            logging.error(f"Cleanup error: {e}")


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python bug_hunter.py <project_directory>")
        print("Example: python bug_hunter.py /path/to/your/python/project")
        sys.exit(1)

    project_dir = sys.argv[1]

    # Validate directory exists
    if not os.path.isdir(project_dir):
        print(f"Error: Directory '{project_dir}' does not exist")
        sys.exit(1)

    try:
        # Initialize the bug hunter
        print(f"Initializing Bug Hunter for directory: {project_dir}")
        hunter = OptimizedBugHunterFixer(project_dir)

        # Get list of Python files
        python_files = list(Path(project_dir).rglob("*.py"))
        print(f"Found {len(python_files)} Python files to process")

        # Process files asynchronously
        print("Starting file processing...")
        asyncio.run(hunter.process_files_async(python_files))

        # Generate and display report
        report = hunter.generate_report()
        print("\nProcessing Report:")
        for key, value in report.items():
            print(f"{key}: {value}")

        # Cleanup
        hunter.cleanup()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)

    def process_batch(self, batch: List[Path]) -> List[Dict[str, Any]]:
        """Process a batch of files with improved error handling."""
        results = []
        for file_path in batch:
            try:
                # Skip files that don't need processing
                if not self.needs_processing(file_path):
                    continue

                result = self.process_single_file(file_path)
                results.append(result)

            except Exception as e:
                logging.error(f"Batch processing error for {file_path}: {e}")
                results.append({"file": file_path, "status": "error", "error": str(e)})
        return results

    def needs_processing(self, file_path: Path) -> bool:
        """Determine if a file needs processing."""
        try:
            # Check file modification time
            if file_path in self.processed_files:
                return False

            # Check if file is in excluded paths
            if any(excluded in str(file_path) for excluded in self.excluded_folders):
                return False

            # Check file size (skip very large files)
            if file_path.stat().st_size > 1_000_000:  # 1MB limit
                logging.warning(f"Skipping large file: {file_path}")
                return False

            return True
        except Exception as e:
            logging.error(f"Error checking file {file_path}: {e}")
            return False

    def process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file with comprehensive error handling."""
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Create backup
            self.backup_file(file_path)

            # Apply formatting
            formatted_content = self.apply_formatting(original_content)

            if formatted_content != original_content:
                # Validate formatted content
                if self.validate_python_syntax(formatted_content):
                    # Write changes
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(formatted_content)

                    return {"file": file_path, "status": "success", "changes": True}
                else:
                    return {
                        "file": file_path,
                        "status": "error",
                        "error": "Invalid formatted content",
                    }

            return {"file": file_path, "status": "success", "changes": False}

        except Exception as e:
            return {"file": file_path, "status": "error", "error": str(e)}

    def apply_formatting(self, content: str) -> str:
        """Apply multiple formatting tools with fallback options."""
        try:
            # Try black formatting
            try:
                content = black.format_str(
                    content,
                    mode=black.FileMode(line_length=88, string_normalization=True),
                )
            except Exception as e:
                logging.warning(f"Black formatting failed: {e}")

            # Try isort
            try:
                content = isort.code(content)
            except Exception as e:
                logging.warning(f"Isort formatting failed: {e}")

            # Try autopep8
            try:
                content = autopep8.fix_code(content, options={"aggressive": 1})
            except Exception as e:
                logging.warning(f"Autopep8 formatting failed: {e}")

            return content

        except Exception as e:
            logging.error(f"Formatting failed: {e}")
            return content

    def validate_python_syntax(self, content: str) -> bool:
        """Validate Python syntax with detailed error reporting."""
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logging.error(f"Syntax validation failed: {e}")
            return False
        except Exception as e:
            logging.error(f"Validation error: {e}")
            return False

    def update_progress(self, current: int, total: int) -> None:
        """Update progress with detailed statistics."""
        try:
            percentage = (current / total) * 100
            elapsed_time = time.time() - self.stats["start_time"]

            if current > 0:
                estimated_total_time = (elapsed_time / current) * total
                remaining_time = estimated_total_time - elapsed_time

                print(
                    f"\rProgress: {percentage:.1f}% "
                    f"({current}/{total} files) "
                    f"| Elapsed: {elapsed_time:.1f}s "
                    f"| Remaining: {remaining_time:.1f}s",
                    end="",
                )
        except Exception as e:
            logging.error(f"Progress update error: {e}")

    def generate_detailed_report(self) -> None:
        """Generate a detailed processing report."""
        try:
            report_path = self.project_dir / "bug_hunter_report.md"

            with open(report_path, "w") as f:
                f.write("# Bug Hunter Processing Report\n\n")

                # Summary statistics
                f.write("## Summary\n")
                f.write(f"- Total files processed: {self._processed_count}\n")
                f.write(
                    f"- Successfully processed: {len(self.stats['success_files'])}\n"
                )
                f.write(f"- Files with errors: {len(self.stats['error_files'])}\n")

                # Performance metrics
                f.write("\n## Performance Metrics\n")
                f.write(
                    f"- Total processing time: {time.time() - self.stats['start_time']:.2f}s\n"
                )
                f.write(
                    f"- Average memory usage: {np.mean(self.stats['memory_usage']):.2f}%\n"
                )
                f.write(
                    f"- Peak memory usage: {max(self.stats['memory_usage']):.2f}%\n"
                )

                # Error summary
                if self.stats["error_files"]:
                    f.write("\n## Error Summary\n")
                    for file_path in self.stats["error_files"]:
                        f.write(f"- {file_path}\n")

            logging.info(f"Detailed report generated: {report_path}")

        except Exception as e:
            logging.error(f"Report generation failed: {e}")


if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description="Python Code Bug Hunter and Fixer")
        parser.add_argument("directory", help="Directory to process")
        parser.add_argument(
            "--backup", action="store_true", help="Create backups before modifications"
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose logging"
        )
        args = parser.parse_args()

        # Configure logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Initialize and run
        hunter = OptimizedBugHunterFixer(args.directory)

        # Get Python files
        python_files = list(Path(args.directory).rglob("*.py"))
        total_files = len(python_files)

        print(f"Found {total_files} Python files to process")

        # Process in batches
        batch_size = 100
        for i in range(0, total_files, batch_size):
            batch = python_files[i : i + batch_size]
            results = hunter.process_batch(batch)

            # Update progress
            hunter.update_progress(i + len(batch), total_files)

        # Generate report
        hunter.generate_detailed_report()

        print("\nProcessing complete! Check bug_hunter_report.md for details.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)
