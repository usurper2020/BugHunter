from .base_tab import BaseTab
from services.analytics_system import AnalyticsSystem
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
value = None
k = 10
content = ""
message = ""
items = []


"""Analytics tab implementation for the BugHunter application."""


class AnalyticsTab(BaseTab):
    """Analytics interface tab"""

    def __init__(self, _analytics_system: AnalyticsSystem, _parent=None):
        self.analytics_system = analytics_system
        self.logger = logging.get_logger("BugHunter.AnalyticsTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create metrics section
            metrics_group = QGroupBox("Key Metrics")
            metrics_layout = QVBoxLayout()
            metrics_group.set_layout(metrics_layout)

            self.metrics_display = QTextEdit()
            self.metrics_display.set_read_only(True)
            self.metrics_display.set_placeholder_text(
                "Metrics will appear here...")
            metrics_layout.add_widget(self.metrics_display)

            # Create visualization controls
            controls_group = QGroupBox("Visualization Controls")
            controls_layout = QVBoxLayout()
            controls_group.set_layout(controls_layout)

            self.time_range_combo = QComboBox()
            self.time_range_combo.add_items(
                ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"]
            )
            self.time_range_combo.current_text_changed.connect(
                self._update_metrics)

            self.refresh_button = QPushButton("Refresh Data")
            self.refresh_button.clicked.connect(self._refresh_metrics)

            controls_layout.add_widget(QLabel("Time Range:"))
            controls_layout.add_widget(self.time_range_combo)
            controls_layout.add_widget(self.refresh_button)

            # Add status section
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.set_layout(status_layout)

            self.status_label = QLabel("Ready")
            self.progress_bar = QProgressBar()
            self.progress_bar.set_range(0, 100)
            self.progress_bar.set_value(0)

            status_layout.add_widget(self.status_label)
            status_layout.add_widget(self.progress_bar)

            # Add all components to main layout
            self.layout.add_widget(metrics_group)
            self.layout.add_widget(controls_group)
            self.layout.add_widget(status_group)

            # Load initial metrics
            self._update_metrics()
            self._update_status("Analytics ready.")

            def _update_metrics(self):
                """Update displayed metrics"""
                try:
                    time_range = self.time_range_combo.current_text()
                    metrics = self.analytics_system.get_metrics(time_range)
                    self.metrics_display.clear()
                    for metric, value in metrics.items():
                        self.metrics_display.append(
                            f"<b>{metric}:</b> {value}")
                        self._update_status("Metrics updated successfully")
                        except Exception as e:
                            self._update_status(
                                f"Error updating metrics: {str(e)}")
                            self.logger.error(
                                f"Error updating metrics: {str(e)}")

                            def _refresh_metrics(self):
                                """Refresh metrics data"""
                                self._update_metrics()

                                def _update_status(self, _message: str):
                                    """Update status message"""
                                    self.status_label.set_text(message)
                                    self.logger.info(message)

                                    def refresh(self):
                                        """Refresh tab content"""
                                        self._update_metrics()
                                        self._update_status(
                                            "Analytics refreshed.")
