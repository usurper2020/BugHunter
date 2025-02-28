# src/services/tool_manager.py
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
import yaml
from PyQt6.QtCore import pyqtSignal, QObject
import logging
from datetime import datetime

class ToolManager(QObject):
    progress_signal = pyqtSignal(str, int)
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    execution_complete_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.tools_dir = Path('tools')
        self.tools_dir.mkdir(exist_ok=True)
        self.installed_tools = {}
        self.logger = logging.getLogger('ToolManager')
        self.active_processes = {}

    def search_github_tools(self, query: str, language: Optional[str] = None) -> Dict[str, Any]:
        try:
            url = f"https://api.github.com/search/repositories?q={query}"
            if language:
                url += f"+language:{language}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {'status': 'success', 'results': data['items']}
        except Exception as e:
            self.logger.error(f"Error searching GitHub tools: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def download_tool(self, repo_url: str) -> Dict[str, Any]:
        try:
            repo_name = repo_url.split('/')[-1]
            download_url = f"{repo_url}/archive/refs/heads/main.zip"
            response = requests.get(download_url)
            response.raise_for_status()

            with tempfile.TemporaryDirectory() as tmpdirname:
                zip_path = Path(tmpdirname) / f"{repo_name}.zip"
                with open(zip_path, 'wb') as f:
                    f.write(response.content)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.tools_dir / repo_name)

            return {'status': 'success', 'tool_name': repo_name}
        except Exception as e:
            self.logger.error(f"Error downloading tool: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def install_tool(self, tool_name: str, tool_metadata: Dict[str, Any]) -> bool:
        tool_path = self.tools_dir / tool_name
        if not tool_path.exists():
            return False

        self.installed_tools[tool_name] = {
            'path': tool_path,
            'metadata': tool_metadata
        }

        if 'dependencies' in tool_metadata:
            self._install_dependencies(tool_metadata['dependencies'])

        return True

    def _install_dependencies(self, dependencies: List[str]) -> bool:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + dependencies)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error installing dependencies: {str(e)}")
            return False

    def execute_tool(self, tool_name: str, args: List[str] = []) -> Optional[str]:
        if tool_name not in self.installed_tools:
            return None

        tool_info = self.installed_tools[tool_name]
        tool_path = tool_info['path']

        entry_points = tool_info['metadata'].get('entry_points', [])
        if not entry_points:
            return None

        main_file = tool_path / entry_points[0]

        try:
            spec = importlib.util.spec_from_file_location(tool_name, main_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[tool_name] = module
            spec.loader.exec_module(module)
            return "Tool executed successfully"
        except Exception as e:
            self.logger.error(f"Error executing tool: {str(e)}")
            return f"Error executing tool: {str(e)}"

    def remove_tool(self, tool_name: str) -> bool:
        if tool_name not in self.installed_tools:
            return False

        tool_path = self.tools_dir / tool_name
        try:
            shutil.rmtree(tool_path)
            del self.installed_tools[tool_name]
            return True
        except OSError as e:
            self.logger.error(f"Error removing tool: {str(e)}")
            return False

    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        return self.installed_tools

    def update_tool(self, tool_name: str) -> bool:
        try:
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                raise ValueError(f"Tool not installed: {tool_name}")

            # Pull latest changes if git repository
            if (tool_path / '.git').exists():
                subprocess.run(
                    ['git', 'pull'],
                    cwd=str(tool_path),
                    check=True,
                    capture_output=True
                )

            # Run update commands if specified
            tool_info = self.installed_tools.get(tool_name, {}).get('metadata', {})
            if 'update_commands' in tool_info:
                for cmd in tool_info['update_commands']:
                    subprocess.run(
                        cmd,
                        shell=True,
                        cwd=str(tool_path),
                        check=True,
                        capture_output=True
                    )

            self.logger.info(f"Tool updated successfully: {tool_name}")
            return True

        except Exception as e:
            self.logger.error(f"Tool update failed - {tool_name}: {str(e)}")
            return False

    def execute_tool(self, tool_name: str, args: List[str] = []) -> Dict[str, Any]:
        if tool_name not in self.installed_tools:
            return {'status': 'error', 'message': f"Tool not installed: {tool_name}"}

        tool_info = self.installed_tools[tool_name]
        tool_path = tool_info['path']

        entry_points = tool_info['metadata'].get('entry_points', [])
        if not entry_points:
            return {'status': 'error', 'message': "No entry points defined for tool"}

        main_file = tool_path / entry_points[0]

        try:
            spec = importlib.util.spec_from_file_location(tool_name, main_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[tool_name] = module
            spec.loader.exec_module(module)
            return {'status': 'success', 'message': "Tool executed successfully"}
        except Exception as e:
            self.logger.error(f"Error executing tool: {str(e)}")
            return {'status': 'error', 'message': f"Error executing tool: {str(e)}"}

    def stop_tool(self, tool_name: str) -> bool:
        if tool_name in self.active_processes:
            process = self.active_processes[tool_name]
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            del self.active_processes[tool_name]
            return True
        return False

    def get_tool_status(self, tool_name: str) -> Dict[str, Any]:
        try:
            if tool_name not in self.installed_tools:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_path = self.tools_dir / tool_name

            return {
                'installed': tool_path.exists(),
                'running': tool_name in self.active_processes,
                'version': self._get_tool_version(tool_name),
                'last_update': self._get_last_update(tool_name)
            }

        except Exception as e:
            self.logger.error(f"Failed to get tool status - {tool_name}: {str(e)}")
            return {'error': str(e)}

    def _get_tool_version(self, tool_name: str) -> Optional[str]:
        try:
            tool_info = self.installed_tools[tool_name]['metadata']
            if 'version_command' in tool_info:
                result = subprocess.run(
                    tool_info['version_command'],
                    shell=True,
                    capture_output=True,
                    text=True
                )
                return result.stdout.strip()
            return None
        except Exception:
            return None

    def _get_last_update(self, tool_name: str) -> Optional[str]:
        try:
            tool_path = self.tools_dir / tool_name
            if tool_path.exists():
                timestamp = tool_path.stat().st_mtime
                return datetime.fromtimestamp(timestamp).isoformat()
            return None
        except Exception:
            return None

    def cleanup(self):
        try:
            for tool_name in list(self.active_processes.keys()):
                self.stop_tool(tool_name)
            self.logger.info("Tool manager resources cleaned up")
        except Exception as e:
            self.logger.error(f"Tool manager cleanup failed: {str(e)}")
