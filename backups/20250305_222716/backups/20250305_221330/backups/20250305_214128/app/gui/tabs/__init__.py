from .wayback_tab import WaybackTab
from .tools_tab import ToolsTab
from .targets_tab import TargetsTab
from .shodan_tab import ShodanTab
from .settings_tab import SettingsTab
from .scope_tab import ScopeTab
from .scanner_tab import ScannerTab
from .nuclei_tab import NucleiTab
from .collaboration_tab import CollaborationTab
from .analytics_tab import AnalyticsTab
from .amass_tab import AmassTab
from .ai_chat_tab import AIChatTab

k = 10
tools = []
"""
This package contains all tab components for the BugHunter application.
"""


__all__ = [
    "AIChatTab",
    "ScannerTab",
    "NucleiTab",
    "AmassTab",
    "ToolsTab",
    "TargetsTab",
    "CollaborationTab",
    "AnalyticsTab",
    "SettingsTab",
    "WaybackTab",
    "ShodanTab",
    "ScopeTab",
]
