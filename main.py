"""
Main entry point for the BugHunter application.

This file implements the main GUI interface using PyQt6, integrating all features
and files within the BugHunter folder. The interface is modular with tabs for
each feature and includes a settings tab for configuration management.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from tabs.ai_chat_tab import AIChatTab
from tabs.nuclei_tab import NucleiTab
from tabs.scanner_tab import ScannerTab
from tabs.tool_manager_tab import ToolManagerTab
from tabs.settings_tab import SettingsTab
from tabs.report_generator_tab import ReportGeneratorTab
from tabs.collaboration_tab import CollaborationTab
from tabs.analytics_tab import AnalyticsTab
from tabs.code_analysis_tab import CodeAnalysisTab
from tabs.vulnerability_tab import VulnerabilityTab



class MainWindow(QMainWindow):
    """
    Main window of the BugHunter application.
    
    This window contains a tabbed interface with the following tabs:
    - AI Chat: Retains and expands the existing AI chat feature
    - Bug Bounty Target: Manages bug bounty targets
    - Nuclei: Integrates Nuclei scanning functionality
    - Scanner: Provides scanning tools
    - Tool Manager: Manages installed tools
    - Settings: Configuration management for all features
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BugHunter")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create main tabs
        self.main_tabs = QTabWidget()
        
        # Create sub-tabs for different categories
        self.scanning_tabs = QTabWidget()
        self.analysis_tabs = QTabWidget()
        self.collab_tabs = QTabWidget()
        
        # Add scanning related tabs
        self.scanning_tabs.addTab(ScannerTab(), "Scanner")
        self.scanning_tabs.addTab(NucleiTab(), "Nuclei")
        self.scanning_tabs.addTab(VulnerabilityTab(), "Vulnerability")
        
        # Add analysis related tabs
        self.analysis_tabs.addTab(CodeAnalysisTab(), "Code Analysis")
        self.analysis_tabs.addTab(AnalyticsTab(), "Analytics")
        self.analysis_tabs.addTab(ReportGeneratorTab(), "Reports")
        
        # Add collaboration related tabs
        self.collab_tabs.addTab(CollaborationTab(), "Collaboration")
        self.collab_tabs.addTab(ToolManagerTab(), "Tools")
        
        # Add main tabs
        self.main_tabs.addTab(self.scanning_tabs, "Scanning")
        self.main_tabs.addTab(self.analysis_tabs, "Analysis")
        self.main_tabs.addTab(self.collab_tabs, "Collaboration")
        self.main_tabs.addTab(AIChatTab(), "AI Chat")
        self.main_tabs.addTab(SettingsTab(), "Settings")
        
        layout.addWidget(self.main_tabs)


def main():
    """
    Application entry point.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
