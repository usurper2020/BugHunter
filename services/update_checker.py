# services/update_checker.py
from PyQt6.QtCore import QObject, pyqtSignal
import aiohttp
import asyncio
from packaging import version
import logging

class UpdateChecker(QObject):
    update_available = pyqtSignal(dict)
    update_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('BugHunter.UpdateChecker')
        self.current_version = "1.0.0"
        self.update_url = "https://api.github.com/repos/yourusername/bughunter/releases/latest"

    def check_updates(self):
        """Check for updates in a non-blocking way"""
        QTimer.singleShot(0, self._check_updates_sync)

    def _check_updates_sync(self):
        """Synchronous update check"""
        try:
            import requests
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name'].strip('v')
                
                needs_update = version.parse(latest_version) > version.parse(self.current_version)
                
                update_info = {
                    "current_version": self.current_version,
                    "latest_version": latest_version,
                    "needs_update": needs_update,
                    "download_url": data['html_url'] if needs_update else None
                }
                self.update_available.emit(update_info)
            else:
                self.update_error.emit(f"HTTP {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            self.update_error.emit(str(e))
