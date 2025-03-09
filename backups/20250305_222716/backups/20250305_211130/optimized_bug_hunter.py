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
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path
from queue import Queue
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, TypeVar, Union

try:
    import autopep8
    import black
    import isort
    import numpy as np
    import psutil
    import pylint.lint
    from tqdm import tqdm
except ImportError as e:
    print(
        f"Error: Required package not found. Please install required packages: {e}")
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

    def start_performance_monitoring(self) -> None:
        """Start comprehensive performance and resource monitoring."""

        def monitor_performance():
            while True:
                try:
                    process = psutil.Process(os.getpid())
                    memory_percent = process.memory_percent()
                    cpu_percent = process.cpu_percent()

                    with self._lock:
                        self.stats["memory_usage"].append(memory_percent)
                        self.stats["cpu_usage"].append(cpu_percent)

                        if memory_percent > self.memory_threshold:
                            self.handle_high_memory_usage()

                    self.perf_logger.info(
                        f"Memory: {memory_percent:.2f}% | "
                        f"CPU: {cpu_percent:.2f}% | "
                        f"Processed: {self._processed_count} | "
                        f"Errors: {self._error_count}"
                    )

                except Exception as e:
                    logging.error(f"Performance monitoring error: {e}")

                time.sleep(self.memory_check_interval)

        threading.Thread(target=monitor_performance, daemon=True).start()

    def setup_logging(self) -> None:
        """Configure advanced logging system with detailed error tracking."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"bughunter_{timestamp}.log"
        error_log = log_dir / f"errors_{timestamp}.log"
        debug_log = log_dir / f"debug_{timestamp}.log"
        perf_log = log_dir / f"performance_{timestamp}.log"

        # Main logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        # Error logger
        error_handler = logging.FileHandler(error_log)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
            )
        )
        logging.getLogger().addHandler(error_handler)

        # Debug logger
        debug_handler = logging.FileHandler(debug_log)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(debug_handler)

        # Performance logger
        self.perf_logger = logging.getLogger("performance")
        perf_handler = logging.FileHandler(perf_log)
        perf_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(message)s"))
        self.perf_logger.addHandler(perf_handler)

    def setup_optimized_environment(self) -> None:
        """Configure system for optimal performance."""
        try:
            process = psutil.Process(os.getpid())

            # Set process priority
            if os.name == "nt":  # Windows
                process.nice(psutil.HIGH_PRIORITY_CLASS)
            else:  # Unix-like
                process.nice(-10)

            # Set CPU affinity
            cpu_count = multiprocessing.cpu_count()
            process.cpu_affinity(list(range(cpu_count)))

            # Increase file handle limit on Unix-like systems
            if os.name != "nt":
                import resource

                resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))

            # Configure garbage collector
            gc.enable()
            gc.set_threshold(700, 10, 5)

            self.start_performance_monitoring()

        except Exception as e:
            logging.warning(f"Environment optimization failed: {e}")

    def handle_high_memory_usage(self) -> None:
        """Handle high memory usage situations."""
        logging.warning("High memory usage detected. Performing cleanup...")

        # Force garbage collection
        gc.collect()

        # Clear caches
        self.file_content_cache.clear()
        self.syntax_tree_cache.clear()
        self.format_cache.clear()
        self.get_file_hash.cache_clear()

        # Reduce batch size
        self.batch_size = max(10, self.batch_size // 2)

        # Additional memory optimization for Windows
        if os.name == "nt":
            import ctypes

            ctypes.windll.psapi.EmptyWorkingSet(
                ctypes.windll.kernel32.GetCurrentProcess()
            )

    def initialize_caches(self) -> None:
        """Initialize enhanced caching system."""
        self.file_content_cache = {}
        self.syntax_tree_cache = {}
        self.pylint_cache = {}
        self.format_cache = {}
        self.error_cache = {}

    def create_backup_directory(self) -> None:
        """Create backup directory with timestamp."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.current_backup_dir = self.backup_dir / timestamp
        self.current_backup_dir.mkdir(parents=True, exist_ok=True)

    @lru_cache(maxsize=1024)
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate and cache file hash."""
        try:
            return hashlib.md5(file_path.read_bytes()).hexdigest()
        except Exception as e:
            logging.debug(f"Hash calculation failed for {file_path}: {e}")
            return ""

    def is_valid_python_file(self, file_path: Path) -> bool:
        """Enhanced Python file validation."""
        try:
            if not file_path.is_file():
                return False
            if file_path.suffix != ".py":
                return False
            if any(part.startswith(".") for part in file_path.parts):
                return False
            if any(excluded in file_path.parts for excluded in self.excluded_folders):
                return False

            # Check file size
            if file_path.stat().st_size > 1024 * 1024 * 10:  # 10MB limit
                logging.warning(f"File too large: {file_path}")
                return False

            # Basic syntax check
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
                return True
            except SyntaxError as e:
                logging.debug(f"Syntax error in {file_path}: {e}")
                return False
            except Exception as e:
                logging.debug(f"Validation error for {file_path}: {e}")
                return False

        except Exception as e:
            logging.debug(f"File validation failed for {file_path}: {e}")
            return False

    async def process_files_async(self, files: List[Path]) -> None:
        """Process files asynchronously with enhanced error handling."""
        try:
            # Filter valid files
            valid_files = [f for f in files if self.is_valid_python_file(f)]
            chunks = np.array_split(
                valid_files, max(1, len(valid_files) // self.batch_size)
            )

            async def process_chunk(chunk: List[Path]):
                tasks = []
                for file in chunk:
                    if not self.is_excluded_path(file):
                        task = self._async_process_file(file)
                        tasks.append(task)
                return await asyncio.gather(*tasks, return_exceptions=True)

            with tqdm(total=len(valid_files), desc="Processing files") as pbar:
                for chunk in chunks:
                    try:
                        results = await process_chunk(list(chunk))
                        self._handle_chunk_results(results)
                        self._update_progress(len(chunk), pbar)
                    except Exception as e:
                        logging.error(f"Chunk processing error: {e}")
                        continue

        except Exception as e:
            logging.error(f"Async processing error: {e}")
            raise

    def backup_file(self, file_path: Path) -> None:
        """Create backup of file before modification."""
        try:
            backup_path = self.current_backup_dir / file_path.relative_to(
                self.project_dir
            )
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil

            shutil.copy2(file_path, backup_path)
        except Exception as e:
            logging.error(f"Backup failed for {file_path}: {e}")

    async def _async_process_file(self, file: Path) -> Dict[str, Any]:
        """Process individual file with comprehensive error handling."""
        start_time = time.time()
        result = {
            "file": file,
            "success": False,
            "errors": [],
            "fixes": [],
            "processing_time": 0,
        }

        try:
            # Create backup before processing
            self.backup_file(file)

            # Read and validate file
            content = await self._read_file_async(file)
            if not content:
                result["errors"].append("Failed to read file")
                return result

            # Process file content
            try:
                fixed_content = await self._apply_fixes_async(content, file)
                if fixed_content != content:
                    await self._write_file_async(file, fixed_content)
                    result["success"] = True
                    result["fixes"].append("Code formatting applied")
            except Exception as e:
                result["errors"].append(f"Fix error: {str(e)}")

            # Run additional checks
            try:
                score = await self._run_pylint_async(file)
                result["pylint_score"] = score
            except Exception as e:
                result["errors"].append(f"Pylint error: {str(e)}")

        except Exception as e:
            result["errors"].append(f"Processing error: {str(e)}")
            logging.error(
                f"Error processing {file}: {e}\n{traceback.format_exc()}")
        finally:
            result["processing_time"] = time.time() - start_time

        return result

    async def _read_file_async(self, file: Path) -> Optional[str]:
        """Read file content asynchronously with enhanced error handling."""
        try:
            if self.use_mmap and file.stat().st_size > 1024 * 1024:  # 1MB
                # Use memory-mapped files for large files
                with open(file, "rb") as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        content = mm.read().decode("utf-8", errors="replace")
            else:
                # Regular file reading for smaller files
                async with asyncio.Lock():
                    with open(file, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()

            if self.use_compression:
                cache_key = self.get_file_hash(file)
                self.file_content_cache[cache_key] = zlib.compress(
                    content.encode())

            return content

        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
            return None

    async def _write_file_async(self, file: Path, content: str) -> bool:
        """Write file content asynchronously with safety checks."""
        try:
            # Create temporary file
            temp_file = file.with_suffix(".tmp")

            try:
                async with asyncio.Lock():
                    with open(temp_file, "w", encoding="utf-8") as f:
                        f.write(content)

                # Verify written content
                with open(temp_file, "r", encoding="utf-8") as f:
                    written_content = f.read()

                if written_content != content:
                    raise ValueError("Content verification failed")

                # Safely replace original file
                temp_file.replace(file)
                return True

            finally:
                if temp_file.exists():
                    temp_file.unlink()

        except Exception as e:
            logging.error(f"Error writing {file}: {e}")
            return False

    def _update_progress(self, count: int, pbar: tqdm) -> None:
        """Update progress bar and statistics."""
        with self._lock:
            self._processed_count += count
            pbar.update(count)

    def _handle_chunk_results(self, results: List[Dict[str, Any]]) -> None:
        """Process and log results from a batch of files."""
        for result in results:
            if isinstance(result, Exception):
                logging.error(f"Chunk processing error: {result}")
                continue

            file_path = result["file"]
            if result["success"]:
                self.stats["success_files"].add(file_path)
                if result.get("fixes"):
                    self.stats["errors_fixed"] += len(result["fixes"])
            else:
                self.stats["error_files"].add(file_path)

            if result.get("errors"):
                for error in result["errors"]:
                    if "syntax error" in error.lower():
                        self.stats["syntax_errors"] += 1
                    elif "import error" in error.lower():
                        self.stats["import_errors"] += 1
                    elif "indentation error" in error.lower():
                        self.stats["indentation_errors"] += 1

    def is_excluded_path(self, path: Path) -> bool:
        """Check if path should be excluded from processing."""
        try:
            return any(excluded in path.parts for excluded in self.excluded_folders)
        except Exception as e:
            logging.error(f"Path exclusion check failed: {e}")
            return True

    def cleanup_resources(self) -> None:
        """Clean up resources and generate final report."""
        try:
            # Stop thread pool
            self.thread_pool.shutdown(wait=True)

            # Stop process pool
            self.process_pool.shutdown(wait=True)

            # Clear caches
            self.file_content_cache.clear()
            self.syntax_tree_cache.clear()
            self.format_cache.clear()
            self.pylint_cache.clear()

            # Force garbage collection
            gc.collect()

            # Generate final report
            self.generate_final_report()

        except Exception as e:
            logging.error(f"Cleanup error: {e}")

    def generate_final_report(self) -> None:
        """Generate comprehensive final report."""
        try:
            end_time = time.time()
            processing_time = end_time - self.stats["start_time"]

            report = [
                "\n=== Bug Hunter Final Report ===",
                f"Total files processed: {len(self.stats['success_files']) + len(self.stats['error_files'])}",
                f"Successfully processed: {len(self.stats['success_files'])}",
                f"Files with errors: {len(self.stats['error_files'])}",
                f"Total processing time: {processing_time:.2f} seconds",
                f"Average memory usage: {np.mean(self.stats['memory_usage']):.2f}%",
                f"Peak memory usage: {max(self.stats['memory_usage']):.2f}%",
                f"Average CPU usage: {np.mean(self.stats['cpu_usage']):.2f}%",
                "\nDetailed error summary:",
                f"Syntax errors: {self.stats['syntax_errors']}",
                f"Import errors: {self.stats['import_errors']}",
                f"Indentation errors: {self.stats['indentation_errors']}",
            ]

            # Write report to file
            report_path = Path("logs") / \
                f"report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("\n".join(report))

            # Log summary
            logging.info("\n".join(report))

        except Exception as e:
            logging.error(f"Report generation error: {e}")


def main():
    """Main execution function with enhanced error handling."""
    try:
        if len(sys.argv) != 2:
            print("Usage: python optimized_bug_hunter.py <project_directory>")
            sys.exit(1)

        project_dir = sys.argv[1]
        if not os.path.isdir(project_dir):
            print(f"Error: Directory '{project_dir}' does not exist")
            sys.exit(1)

        # Initialize and run the bug hunter
        fixer = OptimizedBugHunterFixer(project_dir)

        # Collect Python files
        python_files = list(Path(project_dir).rglob("*.py"))
        if not python_files:
            print("No Python files found in the specified directory")
            sys.exit(0)

        logging.info(f"Found {len(python_files)} Python files to process")

        # Process files
        try:
            asyncio.run(fixer.process_files_async(python_files))
        except KeyboardInterrupt:
            logging.info("Processing interrupted by user")
        except Exception as e:
            logging.error(f"Processing error: {e}")
        finally:
            fixer.cleanup_resources()

    except Exception as e:
        logging.error(f"Critical error: {e}\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
