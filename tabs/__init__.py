"""
BugHunter Tabs Package

This package contains UI tab components for the BugHunter application:
- AI Chat Tab
- Scanner Tab
- Tool Tab
- Amass Tab
- Nuclei Tab
- Tool Manager Tab
"""

from .ai_chat_tab import AIChatTab
from .scanner_tab import ScannerTab
from .tool_tab import ToolTab
from .amass_tab import AmassTab
from .nuclei_tab import NucleiTab
from .tool_manager_tab import ToolManagerTab

__all__ = [
    'AIChatTab',
    'ScannerTab',
    'ToolTab',
    'AmassTab',
    'NucleiTab',
    'ToolManagerTab'
]
