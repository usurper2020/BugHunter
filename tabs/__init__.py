"""
Tabs package for the BugHunter application.
"""

from .ai_chat_tab import AIChatTab
from .nuclei_tab import NucleiTab
from .amass_tab import AmassTab
from .scanner_tab import ScannerTab
from .tool_manager_tab import ToolManagerTab

__all__ = ['AIChatTab', 'NucleiTab', 'AmassTab', 'ScannerTab', 'ToolManagerTab']
