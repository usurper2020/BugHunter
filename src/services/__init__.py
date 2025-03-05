def initialize_services():
    """
    Initializes and imports core services for the BugHunter application.
    This function imports various service modules and defines the `__all__` list 
    to specify the public interface of the services package.
    Imports:
        .ai_system.AISystem
        .nuclei_analyzer.NucleiAnalyzer
        .tool_manager.ToolManager
        .bug_bounty_analyzer.BugBountyAnalyzer
        .code_converter.CodeConverter
        .gui_tab_generator.GUITabGenerator
        .github_manager.GitHubManager
    Defines:
        __all__: List of public objects of the services package.
    """
    from .ai_system import AISystem
    from .nuclei_analyzer import NucleiAnalyzer
    from .tool_manager import ToolManager
    from .bug_bounty_analyzer import BugBountyAnalyzer
    from .code_converter import CodeConverter
    from .gui_tab_generator import GUITabGenerator
    from .github_manager import GitHubManager

    __all__ = [
        'AISystem',
        'NucleiAnalyzer',
        'ToolManager',
        'BugBountyAnalyzer',
        'CodeConverter',
        'GUITabGenerator',
        'GitHubManager'
    ]

initialize_services()
