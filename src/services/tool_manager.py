import subprocess
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil
import os
import requests
import zipfile
import tempfile
import yaml  # Corrected import statement
import logging
from .scan_target import ScanTarget  # Import ScanTarget


class ToolManager:
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.ToolManager')
        self.active_scans = {}  # Dictionary to track active scan targets

    def initialize(self):
        """Initialize the tool manager"""
        self.active_scans = {}

    def add_scan_target(self, target: ScanTarget):
        """Adds a ScanTarget and starts the scan."""
        self.active_scans[target.target_url] = target
        target.start_scan()  # Start the scan for the target
        self.logger.info(f"Started scan for target: {target.target_url}")

    def get_scan_results(self, target: ScanTarget) -> dict:
        """Retrieves results for a specific scan target."""
        if target.target_url in self.active_scans:
            return target.get_results()
        else:
            self.logger.error(
                f"No active scan found for target: {target.target_url}")
            return {'status': 'error', 'error': 'No active scan found'}

    def cancel_scan_target(self, target: ScanTarget):
        """Cancels an ongoing scan for a specific target."""
        if target.target_url in self.active_scans:
            target.cancel_scan()
            del self.active_scans[target.target_url]
            self.logger.info(f"Cancelled scan for target: {target.target_url}")
        else:
            self.logger.error(
                f"No active scan found for target: {target.target_url}")

    def list_active_scans(self) -> List[str]:
        """Returns a list of currently active scan targets and their statuses."""
        return [(target.target_url, target.scan_status) for target in self.active_scans.values()]

    def execute_tool(self, tool_name: str, args: list) -> dict:
        try:
            result = subprocess.run(
                [tool_name] + args, capture_output=True, text=True)
            if result.returncode != 0:
                return {'status': 'error', 'error': result.stderr}
            return {'status': 'success', 'stdout': result.stdout}
        except Exception as e:
            self.logger.error(f"Failed to execute tool {tool_name}: {str(e)}")
            return {'status': 'error', 'error': str(e)}
