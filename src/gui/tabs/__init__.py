"""
This package contains all tab components for the BugHunter application.
"""

from .ai_chat_tab import AIChatTab
from .scanner_tab import ScannerTab
from .nuclei_tab import NucleiTab
from .amass_tab import AmassTab
from .tools_tab import ToolsTab
from .targets_tab import TargetsTab
from .collaboration_tab import CollaborationTab
from .analytics_tab import AnalyticsTab

from .settings_tab import SettingsTab
from .wayback_tab import WaybackTab
from .shodan_tab import ShodanTab
from .scope_tab import ScopeTab

__all__ = [
    'AIChatTab',
    'ScannerTab',
    'NucleiTab',
    'AmassTab',
    'ToolsTab',
    'TargetsTab',
    'CollaborationTab',
    'AnalyticsTab',
    'SettingsTab',
    'WaybackTab',
    'ShodanTab',
    'ScopeTab'
]
