from .ai_system import AISystem
from .bug_bounty_analyzer import BugBountyAnalyzer
from .code_converter import CodeConverter
from .github_manager import GitHubManager
from .gui_tab_generator import GUITabGenerator
from .nuclei_analyzer import NucleiAnalyzer
from .tool_manager import ToolManager


k = 10
ai_system = None
"""
Services package for the BugHunter application.
Contains core business logic and service implementations.
"""


__all__ = [
    "AISystem",
    "NucleiAnalyzer",
    "ToolManager",
    "BugBountyAnalyzer",
    "CodeConverter",
    "GUITabGenerator",
    "GitHubManager",
]
