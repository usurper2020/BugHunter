"""
Tool management service for the BugHunter application.
Handles security tool installation, updates, and execution.
"""

import logging
import yaml
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class ToolManager:
    """Manages security tools and their execution"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.ToolManager')
        self.tools_dir = Path('tools')
        self.tools_dir.mkdir(exist_ok=True)
        self.tools_config = {}
        self.active_processes: Dict[str, subprocess.Popen] = {}
    
    def initialize(self) -> bool:
        """Initialize tool manager and load configurations"""
        try:
            # Load tool configurations
            config_file = Path('config/tools.yml')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.tools_config = yaml.safe_load(f)
            
            # Verify tool installations
            self._verify_installations()
            
            self.logger.info("Tool manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Tool manager initialization failed: {str(e)}")
            return False
    
    def _verify_installations(self):
        """Verify tool installations and their dependencies"""
        for tool_name, tool_info in self.tools_config.items():
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                self.logger.warning(f"Tool not installed: {tool_name}")
                continue
            
            # Verify dependencies
            if 'dependencies' in tool_info:
                for dep in tool_info['dependencies']:
                    try:
                        subprocess.run(
                            ['which', dep],
                            check=True,
                            capture_output=True
                        )
                    except subprocess.CalledProcessError:
                        self.logger.warning(f"Missing dependency for {tool_name}: {dep}")
    
    def install_tool(self, tool_name: str) -> bool:
        """Install a security tool"""
        try:
            if tool_name not in self.tools_config:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            tool_info = self.tools_config[tool_name]
            tool_path = self.tools_dir / tool_name
            
            # Create tool directory
            tool_path.mkdir(exist_ok=True)
            
            # Clone repository if provided
            if 'repository' in tool_info:
                subprocess.run(
                    ['git', 'clone', tool_info['repository'], str(tool_path)],
                    check=True
                )
            
            # Run installation commands
            if 'install_commands' in tool_info:
                for cmd in tool_info['install_commands']:
                    subprocess.run(
                        cmd,
                        shell=True,
                        cwd=str(tool_path),
                        check=True
                    )
            
            self.logger.info(f"Tool installed successfully: {tool_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Tool installation failed - {tool_name}: {str(e)}")
            return False
    
    def update_tool(self, tool_name: str) -> bool:
        """Update a security tool"""
        try:
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                raise ValueError(f"Tool not installed: {tool_name}")
            
            # Pull latest changes if git repository
            if (tool_path / '.git').exists():
                subprocess.run(
                    ['git', 'pull'],
                    cwd=str(tool_path),
                    check=True
                )
            
            # Run update commands if specified
            tool_info = self.tools_config.get(tool_name, {})
            if 'update_commands' in tool_info:
                for cmd in tool_info['update_commands']:
                    subprocess.run(
                        cmd,
                        shell=True,
                        cwd=str(tool_path),
                        check=True
                    )
            
            self.logger.info(f"Tool updated successfully: {tool_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Tool update failed - {tool_name}: {str(e)}")
            return False
    
    def execute_tool(self, tool_name: str, args: List[str]) -> Dict[str, Any]:
        """Execute a security tool with given arguments"""
        try:
            if tool_name not in self.tools_config:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            tool_info = self.tools_config[tool_name]
            tool_path = self.tools_dir / tool_name
            
            # Build command
            cmd = [tool_info['executable']] + args
            
            # Start process
            process = subprocess.Popen(
                cmd,
                cwd=str(tool_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Store process
            self.active_processes[tool_name] = process
            
            # Wait for completion
            stdout, stderr = process.communicate()
            
            # Remove from active processes
            del self.active_processes[tool_name]
            
            return {
                'status': 'success' if process.returncode == 0 else 'error',
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            }
            
        except Exception as e:
            self.logger.error(f"Tool execution failed - {tool_name}: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def stop_tool(self, tool_name: str) -> bool:
        """Stop a running tool process"""
        try:
            if tool_name in self.active_processes:
                process = self.active_processes[tool_name]
                process.terminate()
                process.wait(timeout=5)
                del self.active_processes[tool_name]
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to stop tool - {tool_name}: {str(e)}")
            return False
    
    def get_tool_status(self, tool_name: str) -> Dict[str, Any]:
        """Get status of a tool"""
        try:
            if tool_name not in self.tools_config:
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
            return {
                'error': str(e)
            }
    
    def _get_tool_version(self, tool_name: str) -> Optional[str]:
        """Get version of installed tool"""
        try:
            tool_info = self.tools_config[tool_name]
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
        """Get last update timestamp of tool"""
        try:
            tool_path = self.tools_dir / tool_name
            if tool_path.exists():
                timestamp = tool_path.stat().st_mtime
                return datetime.fromtimestamp(timestamp).isoformat()
            return None
        except Exception:
            return None
    
    def cleanup(self):
        """Cleanup tool manager resources"""
        try:
            # Stop all running processes
            for tool_name in list(self.active_processes.keys()):
                self.stop_tool(tool_name)
            
            self.logger.info("Tool manager resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Tool manager cleanup failed: {str(e)}")
