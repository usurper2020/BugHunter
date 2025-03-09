from .base_tab import BaseTab
from services.config_manager import ConfigManager
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
default = None
k = 10
content = ""
message = ""


"""Settings tab implementation for the BugHunter application."""


class SettingsTab(BaseTab):
    """Settings management interface tab"""

    def __init__(self, _config_manager: ConfigManager, _parent=None):
        self.config_manager = config_manager
        self.logger = logging.get_logger("BugHunter.SettingsTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create settings form section
            settings_group = QGroupBox("Application Settings")
            settings_layout = QFormLayout()
            settings_group.set_layout(settings_layout)

            # Add settings controls
            self.theme_combo = QComboBox()
            self.theme_combo.add_items(["Dark", "Light", "System"])
            settings_layout.add_row("Theme:", self.theme_combo)

            self.auto_update_check = QCheckBox("Enable automatic updates")
            settings_layout.add_row(self.auto_update_check)

            self.log_level_combo = QComboBox()
            self.log_level_combo.add_items(
                ["DEBUG", "INFO", "WARNING", "ERROR"])
            settings_layout.add_row("Log Level:", self.log_level_combo)

            # Create save/restore section
            action_group = QGroupBox("Actions")
            action_layout = QVBoxLayout()
            action_group.set_layout(action_layout)

            self.save_button = QPushButton("Save Settings")
            self.save_button.clicked.connect(self._save_settings)

            self.restore_button = QPushButton("Restore Defaults")
            self.restore_button.clicked.connect(self._restore_defaults)

            action_layout.add_widget(self.save_button)
            action_layout.add_widget(self.restore_button)

            # Add status section
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.set_layout(status_layout)

            self.status_label = QLabel("Ready")
            status_layout.add_widget(self.status_label)

            # Add all components to main layout
            self.layout.add_widget(settings_group)
            self.layout.add_widget(action_group)
            self.layout.add_widget(status_group)

            # Load current settings
            self._load_settings()
            self._update_status("Settings manager ready.")

            def _load_settings(self):
                """Load current settings from config manager"""
                try:
                    config = self.config_manager.get_config()
                    self.theme_combo.set_current_text(
                        config.get("theme", "Dark"))
                    self.auto_update_check.set_checked(
                        config.get("auto_update", True))
                    self.log_level_combo.set_current_text(
                        config.get("log_level", "INFO"))
                    self._update_status("Settings loaded successfully")
                    except Exception as e:
                        self._update_status(
                            f"Error loading settings: {str(e)}")
                        self.logger.error(f"Error loading settings: {str(e)}")

                        def _update_status(self, _message: str):
                            """Update status message"""
                            self.status_label.set_text(message)
                            self.logger.info(message)

                            @pyqt_slot()
                            def _save_settings(self):
                                """Handle saving settings"""
                                try:
                                    config = {
                                        "theme": self.theme_combo.current_text(),
                                        "auto_update": self.auto_update_check.is_checked(),
                                        "log_level": self.log_level_combo.current_text(),
                                    }
                                    self.config_manager.save_config(config)
                                    self._update_status(
                                        "Settings saved successfully")
                                    except Exception as e:
                                        self._update_status(
                                            f"Error saving settings: {str(e)}")
                                        self.logger.error(
                                            f"Error saving settings: {str(e)}")

                                        @pyqt_slot()
                                        def _restore_defaults(self):
                                            """Handle restoring default settings"""
                                            try:
                                                self.config_manager.restore_defaults()
                                                self._load_settings()
                                                self._update_status(
                                                    "Default settings restored")
                                                except Exception as e:
                                                    self._update_status(
                                                        f"Error restoring defaults: {str(e)}")
                                                    self.logger.error(
                                                        f"Error restoring defaults: {str(e)}")

                                                    def refresh(self):
                                                        """Refresh tab content"""
                                                        self._load_settings()
                                                        self._update_status(
                                                            "Settings manager refreshed.")
