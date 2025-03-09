import array
import asyncio
import io
import logging
import msvcrt
import multiprocessing
import os
import shutil
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import lru_cache, partial
from pathlib import Path
from typing import Any, Dict, List

import autopep8
import black
import isort
import psutil
import win32api
import win32con
import win32process
import xxhash
from tqdm import tqdm


class WindowsFastBugHunter:
    __slots__ = (
        "project_dir",
        "stats",
        "pools",
        "backup_dir",
        "io_config",
        "formatters",
        "batch_size",
        "temp_dir",
        "buffer",
    )

    def __init__(self, project_dir: str):
        self._optimize_windows()
        self.project_dir = Path(project_dir).resolve()
        self.stats = array.array("Q", [0] * 4)  # unsigned long long array

        # Optimized buffer for Windows
        self.buffer = memoryview(bytearray(262144))  # 256KB buffer

        # Fast temp directory
        self.temp_dir = Path(tempfile.gettempdir()) / "bughunter_temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # CPU optimization
        cpu_count = psutil.cpu_count(logical=False)
        self.batch_size = 4096  # Optimized for Windows

        # Windows-optimized thread pools
        self.pools = {
            "io": ThreadPoolExecutor(
                max_workers=cpu_count * 2, thread_name_prefix="io"
            ),
            "cpu": ProcessPoolExecutor(
                max_workers=cpu_count, mp_context=multiprocessing.get_context("spawn")
            ),
        }

        # Pre-initialized formatters
        self.formatters = {
            "black": black.FileMode(line_length=88),
            "isort": {
                "profile": "black",
                "multi_line_output": 3,
                "include_trailing_comma": True,
                "force_grid_wrap": 0,
                "use_parentheses": True,
                "ensure_newline_before_comments": True,
                "line_length": 88,
            },
        }

        # Windows-optimized I/O
        self.io_config = {
            "buffer_size": 262144,  # 256KB buffer
            "encoding": "utf-8",
            "errors": "ignore",
        }

        # Setup backup directory
        self.backup_dir = self._setup_backup_dir()

    def _optimize_windows(self):
        """Windows-specific optimizations."""
        # Set process priority
        handle = win32api.GetCurrentProcess()
        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)

        # Optimize I/O
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # Increase working set size
        win32process.SetProcessWorkingSetSize(handle, -1, -1)

        # Disable file system redirection
        import ctypes

        wow64 = ctypes.c_long(0)
        ctypes.windll.kernel32.Wow64DisableWow64FsRedirection(ctypes.byref(wow64))

    def _setup_backup_dir(self) -> Path:
        """Fast backup directory setup."""
        backup_dir = self.project_dir / "backups" / str(int(time.time()))
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    @lru_cache(maxsize=1024)
    def _fast_hash(self, data: bytes) -> str:
        """Fast file hashing using xxhash."""
        return xxhash.xxh3_64_hexdigest(data)

    async def _fast_read(self, path: Path) -> str:
        """Windows-optimized file reading."""
        try:
            # Use binary mode for better performance
            with open(path, "rb", buffering=self.io_config["buffer_size"]) as f:
                content = f.read()
                return content.decode("utf-8", errors="ignore")
        except Exception as e:
            logging.error(f"Read error {path}: {e}")
            return ""

    async def _fast_write(self, path: Path, content: str) -> bool:
        """Windows-optimized file writing."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file first
            temp_path = (
                self.temp_dir
                / f"{path.stem}_{self._fast_hash(str(path).encode())}{path.suffix}"
            )

            with open(temp_path, "w", **self.io_config) as f:
                f.write(content)

            # Atomic move
            shutil.move(str(temp_path), str(path))
            return True
        except Exception as e:
            logging.error(f"Write error {path}: {e}")
            return False

    async def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Optimized single file processing."""
        try:
            if not file_path.suffix == ".py":
                return {"status": "skipped", "file": file_path}

            content = await self._fast_read(file_path)
            if not content:
                return {"status": "error", "file": file_path}

            # Format content
            try:
                formatted = black.format_str(content, mode=self.formatters["black"])
                formatted = isort.code(formatted, **self.formatters["isort"])
                formatted = autopep8.fix_code(formatted)
            except Exception as e:
                return {"status": "error", "file": file_path, "error": str(e)}

            if formatted == content:
                return {"status": "unchanged", "file": file_path}

            # Backup original
            backup_path = self.backup_dir / file_path.relative_to(self.project_dir)
            await self._fast_write(backup_path, content)

            if await self._fast_write(file_path, formatted):
                return {"status": "success", "file": file_path}
            return {"status": "error", "file": file_path}

        except Exception as e:
            return {"status": "error", "file": file_path, "error": str(e)}

    async def process_files(self, files: List[Path]) -> None:
        """Batch processing optimized for Windows."""
        try:
            python_files = [f for f in files if f.suffix == ".py"]
            if not python_files:
                print("No Python files found")
                return

            with tqdm(total=len(python_files), desc="Processing", unit="files") as pbar:
                # Process in batches
                for i in range(0, len(python_files), self.batch_size):
                    batch = python_files[i : i + self.batch_size]
                    tasks = [self.process_file(file) for file in batch]

                    results = await asyncio.gather(*tasks)

                    # Update progress and stats
                    pbar.update(len(batch))
                    self._update_stats(results)

        finally:
            await self._cleanup()

    def _update_stats(self, results: List[Dict[str, Any]]) -> None:
        """Fast statistics update."""
        for result in results:
            if result["status"] == "success":
                self.stats[0] += 1
            elif result["status"] == "error":
                self.stats[1] += 1
            else:
                self.stats[2] += 1
            self.stats[3] += 1

    async def _cleanup(self) -> None:
        """Resource cleanup."""
        for pool in self.pools.values():
            pool.shutdown(wait=False)

        # Clean temp directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)

        # Generate report
        report = f"""Bug Hunter Report
================
Processed: {self.stats[3]}
Success: {self.stats[0]}
Errors: {self.stats[1]}
Skipped: {self.stats[2]}"""

        await self._fast_write(self.project_dir / "bug_hunter_report.txt", report)


async def main():
    """Windows-optimized main execution."""
    try:
        # Minimal logging
        logging.basicConfig(level=logging.ERROR)

        hunter = WindowsFastBugHunter(".")
        files = list(Path(".").rglob("*.py"))

        if files:
            print(f"Processing {len(files)} Python files...")
            await hunter.process_files(files)
            print("\nDone! Check bug_hunter_report.txt for details.")
        else:
            print("No Python files found")

    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    # Windows-compatible event loop
    asyncio.run(main())
