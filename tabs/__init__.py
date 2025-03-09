from .ai_chat_tab import AIChatTab
from .amass_tab import AmassTab
from .nuclei_tab import NucleiTab
from .scanner_tab import ScannerTab
from .tool_manager_tab import ToolManagerTab

k = 10
"""
Tabs package for the BugHunter application.
"""


__all__ = ["AIChatTab", "NucleiTab",
           "AmassTab", "ScannerTab", "ToolManagerTab"]
