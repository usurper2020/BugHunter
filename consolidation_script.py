#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Project Backup and Consolidation System
Version: 2.0
"""

import asyncio
import bz2
import gzip
import hashlib
import json
import logging
import lzma
import os
import re
import shutil
import socket
import ssl
import subprocess
import tempfile
import time
from base64 import urlsafe_b64encode
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from filecmp import dircmp
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

import aiohttp
import yaml
import zipfile
import sys
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backup_manager.log')
    ]
)
logger = logging.getLogger(__name__)

# Dataclass definitions
@dataclass
class ToolInfo:
    name: str
    version: str
    path: str
    dependencies: List[str]
    last_update: datetime
    status: str

@dataclass
class BugBountyTarget:
    name: str
    url: str
    scope: List[str]
    out_of_scope: List[str]
    reward_range: Tuple[float, float]
    platform: str
    start_date: datetime
    end_date: Optional[datetime]

@dataclass
class AIModel:
    name: str
    provider: str
    api_key: str
    capabilities: List[str]
    context_window: int
    max_tokens: int
    temperature: float

@dataclass
class SecurityScan:
    target: str
    scan_type: str
    start_time: datetime
    end_time: Optional[datetime]
    findings: List[Dict]
    severity_counts: Dict[str, int]

@dataclass
class BackupMetadata:
    timestamp: str
    hash: str
    size: int
    files_count: int
    directories_count: int
    backup_type: str
    compression_type: str
    encrypted: bool = False
    differential_base: Optional[str] = None

@dataclass
class BackupProgress:
    total_files: int = 0
    processed_files: int = 0
    current_file: str = ""
    status: str = "pending"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)

    @property
    def progress_percentage(self) -> float:
        if self.total_files == 0:
            return 0.0
        return (self.processed_files / self.total_files) * 100

    @property
    def elapsed_time(self) -> Optional[timedelta]:
        if self.start_time is None:
            return None
        end = self.end_time or datetime.now()
        return end - self.start_time

class BackupManager:
    """Enhanced backup management system with advanced features"""

    @dataclass
    class BackupConfig:
        max_backups: int = 5
        compression_level: int = 9
        chunk_size: int = 8192
        exclude_patterns: List[str] = field(default_factory=lambda: [
            '*__pycache__*', '*.pyc', '*.pyo', '*.pyd',
            '.git', '.idea', '.vscode', 'venv', 'backups'
        ])
        backup_schedule: str = "0 0 * * *"  # Daily at midnight
        encryption_enabled: bool = False
        encryption_key: Optional[str] = None
        compression_algorithm: str = 'zip'  # 'zip', 'gzip', 'bz2', 'lzma'
        verify_after_backup: bool = True
        differential_backup_enabled: bool = True
        max_differential_count: int = 5
        async_backup: bool = True
        progress_callback: Optional[callable] = None

    def __init__(self, project_root: Path):
        """Initialize the backup manager with enhanced configuration"""
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / 'backups'
    # Create parent directories if they don't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.backup_dir / 'backup_metadata.json'
        self.config = self.BackupConfig()
        self.progress = BackupProgress()
        self.metadata = {'backups': [], 'config_version': '2.0'}
        
        # Initialize encryption if enabled
        if self.config.encryption_enabled and self.config.encryption_key:
            self.fernet = Fernet(urlsafe_b64encode(
                hashlib.sha256(self.config.encryption_key.encode()).digest()
            ))
        else:
            self.fernet = None

    def load_metadata(self) -> None:
        """Load backup metadata with error handling"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {'backups': [], 'config_version': '2.0'}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse metadata file: {e}")
            # Create backup of corrupted metadata
            if self.metadata_file.exists():
                shutil.copy2(
                    self.metadata_file,
                    self.metadata_file.with_suffix('.json.bak')
                )
            self.metadata = {'backups': [], 'config_version': '2.0'}
        except Exception as e:
            logger.error(f"Unexpected error loading metadata: {e}")
            self.metadata = {'backups': [], 'config_version': '2.0'}

    def save_metadata(self) -> None:
        """Save backup metadata with atomic write"""
        temp_file = self.metadata_file.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                json.dump(self.metadata, f, indent=4)
            # Atomic replace
            temp_file.replace(self.metadata_file)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise

    async def create_async_backup(self) -> Tuple[Path, Path, BackupMetadata]:
        """Create backup asynchronously with progress tracking"""
        self.progress = BackupProgress()
        self.progress.start_time = datetime.now()
        self.progress.status = "starting"

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'project_backup_{timestamp}'
        
        try:
            # Count total files for progress tracking
            self.progress.total_files = sum(
                1 for _ in self.project_root.rglob('*') 
                if _.is_file() and not any(
                    pattern in str(_) for pattern in self.config.exclude_patterns
                )
            )

            # Create temporary directory for backup
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_backup_path = Path(temp_dir) / backup_name
                dir_backup_path = self.backup_dir / backup_name
                zip_backup_path = self.backup_dir / f'{backup_name}.zip'

                # Copy files with progress tracking
                await self._async_copy_files(self.project_root, temp_backup_path)

                # Calculate directory hash
                dir_hash = await self._async_calculate_hash(temp_backup_path)

                # Create zip backup with selected compression
                await self._async_create_compressed_backup(
                    temp_backup_path, zip_backup_path
                )

                # Move directory backup to final location
                await asyncio.to_thread(
                    shutil.move, temp_backup_path, dir_backup_path
                )

                # Create metadata
                metadata = await self._create_backup_metadata(
                    timestamp, dir_hash, dir_backup_path
                )

                # Update metadata file
                self.metadata['backups'].append({
                    'timestamp': timestamp,
                    'dir_path': str(dir_backup_path),
                    'zip_path': str(zip_backup_path),
                    **asdict(metadata)
                })
                await asyncio.to_thread(self.save_metadata)

                self.progress.status = "completed"
                self.progress.end_time = datetime.now()

                return dir_backup_path, zip_backup_path, metadata

        except Exception as e:
            self.progress.status = "failed"
            self.progress.errors.append(str(e))
            self.progress.end_time = datetime.now()
            logger.error(f"Async backup failed: {e}")
            raise

    async def _async_copy_files(self, source: Path, dest: Path) -> None:
        """Copy files asynchronously with progress tracking"""
        async def copy_file(src: Path, dst: Path):
            self.progress.current_file = str(src)
            await asyncio.to_thread(shutil.copy2, src, dst)
            self.progress.processed_files += 1
            if self.config.progress_callback:
                self.config.progress_callback(self.progress)

        # Create destination directory if it doesn't exist
        dest.mkdir(parents=True, exist_ok=True)

        tasks = []
        for src_path in source.rglob('*'):
            if src_path.is_file() and not any(
                pattern in str(src_path) for pattern in self.config.exclude_patterns
            ):
                rel_path = src_path.relative_to(source)
                dst_path = dest / rel_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                tasks.append(copy_file(src_path, dst_path))

        if tasks:
            await asyncio.gather(*tasks)

    async def _async_calculate_hash(self, directory: Path) -> str:
        """Calculate directory hash asynchronously"""
        hash_obj = hashlib.sha256()
        
        for root, _, files in os.walk(directory):
            for file in sorted(files):  # Sort for consistent hashing
                file_path = Path(root) / file
                if file_path.is_file():
                    async with aiofiles.open(file_path, 'rb') as f:
                        while chunk := await f.read(self.config.chunk_size):
                            hash_obj.update(chunk)
        
        return hash_obj.hexdigest()

    async def _create_backup_metadata(
        self, timestamp: str, dir_hash: str, backup_path: Path
    ) -> BackupMetadata:
        """Create backup metadata"""
        try:
            files_count = sum(1 for _ in backup_path.rglob('*') if _.is_file())
            directories_count = sum(1 for _ in backup_path.rglob('*') if _.is_dir())
            total_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())

            return BackupMetadata(
                timestamp=timestamp,
                hash=dir_hash,
                size=total_size,
                files_count=files_count,
                directories_count=directories_count,
                backup_type='full',
                compression_type=self.config.compression_algorithm,
                encrypted=self.config.encryption_enabled
            )
        except Exception as e:
            logger.error(f"Failed to create backup metadata: {e}")
            raise

    async def _async_create_compressed_backup(
        self, source_path: Path, dest_path: Path
    ) -> None:
        """Create compressed backup using selected algorithm"""
        if self.config.compression_algorithm == 'zip':
            await self._create_zip_backup(source_path, dest_path)
        else:
            await self._create_alternative_compressed_backup(
                source_path, dest_path
            )

    async def _create_zip_backup(self, source_path: Path, dest_path: Path) -> None:
        """Create ZIP backup with progress tracking"""
        def zip_files():
            with zipfile.ZipFile(
                dest_path, 'w',
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=self.config.compression_level
            ) as zipf:
                for file_path in source_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_path)
                        zipf.write(file_path, arcname)

        await asyncio.to_thread(zip_files)

    async def _create_alternative_compressed_backup(
        self, source_path: Path, dest_path: Path
    ) -> None:
        """Create backup with alternative compression algorithms"""
        compression_map = {
            'gzip': (gzip.open, '.gz'),
            'bz2': (bz2.open, '.bz2'),
            'lzma': (lzma.open, '.xz')
        }

        if self.config.compression_algorithm not in compression_map:
            raise ValueError(f"Unsupported compression: {self.config.compression_algorithm}")

        compress_func, extension = compression_map[self.config.compression_algorithm]
        final_path = dest_path.with_suffix(extension)

        async def compress_file(src: Path, dst: Path):
            with open(src, 'rb') as f_in:
                with compress_func(dst, 'wb') as f_out:
                    while chunk := f_in.read(self.config.chunk_size):
                        f_out.write(chunk)

        await asyncio.to_thread(compress_file, source_path, final_path)

    async def create_differential_backup(self, base_backup_path: Path) -> Tuple[Path, BackupMetadata]:
        """Create a differential backup based on a full backup"""
        if not self.config.differential_backup_enabled:
            raise ValueError("Differential backup is not enabled in configuration")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        diff_backup_name = f'differential_backup_{timestamp}'
        diff_backup_path = self.backup_dir / diff_backup_name

        try:
            # Get different files
            different_files = await self._get_different_files(base_backup_path)
            
            # Create differential backup
            diff_backup_path.mkdir(parents=True)
            
            for file_path in different_files:
                source = self.project_root / file_path
                destination = diff_backup_path / file_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                await asyncio.to_thread(shutil.copy2, source, destination)

            # Calculate metadata
            dir_hash = await self._async_calculate_hash(diff_backup_path)
            
            metadata = BackupMetadata(
                timestamp=timestamp,
                hash=dir_hash,
                size=sum(f.stat().st_size for f in diff_backup_path.rglob('*') if f.is_file()),
                files_count=len(different_files),
                directories_count=sum(1 for _ in diff_backup_path.rglob('*') if _.is_dir()),
                backup_type='differential',
                compression_type='none',
                differential_base=str(base_backup_path)
            )

            # Update metadata
            self.metadata['backups'].append({
                'timestamp': timestamp,
                'dir_path': str(diff_backup_path),
                'differential_base': str(base_backup_path),
                **asdict(metadata)
            })
            await asyncio.to_thread(self.save_metadata)

            return diff_backup_path, metadata

        except Exception as e:
            logger.error(f"Differential backup failed: {e}")
            if diff_backup_path.exists():
                shutil.rmtree(diff_backup_path)
            raise

    async def _get_different_files(self, base_path: Path) -> Set[Path]:
        """Get files that are different from base backup"""
        different_files = set()

        def compare_directories(dcmp: dircmp) -> Set[Path]:
            different = set()
            
            # Add modified and new files
            different.update(dcmp.diff_files)
            different.update(dcmp.left_only)
            
            # Recursively check subdirectories
            for sub_dcmp in dcmp.subdirs.values():
                different.update(compare_directories(sub_dcmp))
                
            return different

        comparison = await asyncio.to_thread(
            dircmp, self.project_root, base_path
        )
        return await asyncio.to_thread(compare_directories, comparison)

    async def verify_backup_integrity(self, backup_path: Path) -> Dict[str, Any]:
        """Perform comprehensive backup validation"""
        validation_results = {
            'size_check': False,
            'hash_check': False,
            'content_check': False,
            'metadata_check': False,
            'encryption_check': False,
            'errors': []
        }

        try:
            # Size check
            actual_size = backup_path.stat().st_size
            expected_size = next(
                (b['size'] for b in self.metadata['backups'] 
                 if b['dir_path'] == str(backup_path) 
                 or b['zip_path'] == str(backup_path)),
                None
            )
            validation_results['size_check'] = actual_size == expected_size

            # Hash check
            current_hash = await self._async_calculate_hash(backup_path)
            stored_hash = next(
                (b['hash'] for b in self.metadata['backups']
                 if b['dir_path'] == str(backup_path)
                 or b['zip_path'] == str(backup_path)),
                None
            )
            validation_results['hash_check'] = current_hash == stored_hash

            # Content check
            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    validation_results['content_check'] = zipf.testzip() is None
            else:
                validation_results['content_check'] = True

            # Metadata check
            validation_results['metadata_check'] = any(
                b['dir_path'] == str(backup_path) or b['zip_path'] == str(backup_path)
                for b in self.metadata['backups']
            )

            # Encryption check
            if self.config.encryption_enabled:
                validation_results['encryption_check'] = await self._verify_encryption(backup_path)

        except Exception as e:
            validation_results['errors'].append(str(e))
            logger.error(f"Backup validation failed: {e}")

        return validation_results

class ProjectConsolidator:
    """Handles project consolidation and organization"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.backup_manager = BackupManager(project_root)
        
    async def consolidate_project(self) -> Dict[str, Any]:
        """Consolidate project files and create organized structure"""
        consolidation_result = {
            'organized_files': 0,
            'removed_duplicates': 0,
            'cleaned_temp_files': 0,
            'errors': []
        }

        try:
            # Create backup before consolidation
            await self.backup_manager.create_async_backup()

            # Organize files by type
            await self._organize_by_type()
            
            # Remove duplicate files
            duplicates = await self._find_duplicates()
            await self._remove_duplicates(duplicates)
            
            # Clean temporary files
            await self._clean_temp_files()
            
            # Update consolidation results
            consolidation_result.update({
                'organized_files': sum(1 for _ in self.project_root.rglob('*') if _.is_file()),
                'removed_duplicates': len(duplicates),
                'cleaned_temp_files': await self._count_cleaned_files()
            })

        except Exception as e:
            consolidation_result['errors'].append(str(e))
            logger.error(f"Project consolidation failed: {e}")

        return consolidation_result

    async def _organize_by_type(self) -> None:
        """Organize files by their type into appropriate directories"""
        type_dirs = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rst'],
            'source': ['.py', '.js', '.java', '.cpp', '.h', '.css', '.html'],
            'data': ['.json', '.yaml', '.yml', '.xml', '.csv', '.sqlite'],
            'archives': ['.zip', '.tar', '.gz', '.bz2', '.xz', '.7z']
        }

        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                for dir_name, extensions in type_dirs.items():
                    if file_ext in extensions:
                        new_dir = self.project_root / dir_name
                        new_dir.mkdir(exist_ok=True)
                        new_path = new_dir / file_path.name
                        
                        if new_path.exists():
                            new_path = new_dir / f"{file_path.stem}_{int(time.time())}{file_ext}"
                        
                        await asyncio.to_thread(shutil.move, file_path, new_path)
                        break

    async def _find_duplicates(self) -> Dict[str, List[Path]]:
        """Find duplicate files using hash comparison"""
        hash_dict: Dict[str, List[Path]] = {}
        
        async def calculate_file_hash(file_path: Path) -> Tuple[str, Path]:
            hash_obj = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_obj.update(chunk)
            return (hash_obj.hexdigest(), file_path)

        # Create tasks for all files
        tasks = [
            calculate_file_hash(f) 
            for f in self.project_root.rglob('*') 
            if f.is_file()
        ]
        
        # Execute tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Group files by hash
        for file_hash, file_path in results:
            hash_dict.setdefault(file_hash, []).append(file_path)
            
        # Return only duplicates
        return {h: paths for h, paths in hash_dict.items() if len(paths) > 1}

    async def _remove_duplicates(self, duplicates: Dict[str, List[Path]]) -> None:
        """Remove duplicate files keeping the oldest version"""
        for hash_value, file_paths in duplicates.items():
            # Sort by creation time, keep the oldest
            sorted_paths = sorted(file_paths, key=lambda p: p.stat().st_ctime)
            # Remove duplicates
            for path in sorted_paths[1:]:
                await asyncio.to_thread(path.unlink)

    async def _clean_temp_files(self) -> None:
        """Clean temporary and unnecessary files"""
        temp_patterns = [
            '*.tmp', '*.temp', '*.bak', '*.swp',
            '~*', '*.cache', '*.log', '*.pyc',
            '__pycache__', '.DS_Store'
        ]

        for pattern in temp_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    await asyncio.to_thread(file_path.unlink)
                elif file_path.is_dir():
                    await asyncio.to_thread(shutil.rmtree, file_path)

    async def _count_cleaned_files(self) -> int:
        """Count number of cleaned temporary files"""
        return sum(1 for _ in self.project_root.rglob('*') if _.is_file())

# Utility functions for the entire system
async def verify_system_requirements() -> Dict[str, bool]:
    """Verify system requirements for backup and consolidation"""
    requirements = {
        'python_version': False,
        'disk_space': False,
        'permissions': False,
        'dependencies': False
    }

    # Check Python version
    requirements['python_version'] = sys.version_info >= (3, 11, 9)

    # Check available disk space
    try:
        total, used, free = shutil.disk_usage('/')
        requirements['disk_space'] = free > (10 * 1024 * 1024 * 1024)  # 10GB
    except Exception:
        pass

    # Check permissions
    try:
        test_file = Path('test_permissions.tmp')
        test_file.touch()
        test_file.unlink()
        requirements['permissions'] = True
    except Exception:
        pass

    # Check dependencies
    try:
        import aiofiles
        import cryptography
        requirements['dependencies'] = True
    except ImportError:
        pass

    return requirements

# Example usage
async def main():
    # Initialize project root and create it if it doesn't exist
    project_root = Path('my_project').absolute()
    project_root.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Initializing project in: {project_root}")
    
    # Verify system requirements
    requirements = await verify_system_requirements()
    if not all(requirements.values()):
        logger.error("System requirements not met:")
        for req, status in requirements.items():
            logger.error(f"{req}: {'✓' if status else '✗'}")
        return

    try:
        # Initialize consolidator
        consolidator = ProjectConsolidator(project_root)
        
        # Perform consolidation
        result = await consolidator.consolidate_project()
        
        # Log results
        logger.info(f"Consolidation completed: {result}")
        
    except Exception as e:
        logger.error(f"Consolidation failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

