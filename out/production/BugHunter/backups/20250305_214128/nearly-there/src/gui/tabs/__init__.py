from .ai_chat_tab import AIChatTab
from .amass_tab import AmassTab
from .analytics_tab import AnalyticsTab
from .collaboration_tab import CollaborationTab
from .nuclei_tab import NucleiTab
from .scanner_tab import ScannerTab
from .scope_tab import ScopeTab
from .settings_tab import SettingsTab
from .shodan_tab import ShodanTab
from .targets_tab import TargetsTab
from .tools_tab import ToolsTab
from .wayback_tab import WaybackTab


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
