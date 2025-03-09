from services.analytics_system import AnalyticsSystem
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

status = "active"
value = None
k = 10
tools = []
"""
Analytics tab for the BugHunter application.

This tab provides tools for data analysis and visualization with real-time
status updates and interactive controls.
"""


class AnalyticsTab(QWidget):
    """
    Tab widget providing comprehensive data analysis functionality.

        Features:
        - Real-time data visualization
        - Interactive charts
        - Data filtering
        - Progress tracking
        - Status updates
    """

    def __init__(self):
        super().__init__()
        self.analytics = AnalyticsSystem()
        self.init_ui()
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)

        def init_ui(self):
            """Initialize the UI components with enhanced status tracking."""
            main_layout = QVBoxLayout()

            # Create a splitter for better layout management
            splitter = QSplitter()
            splitter.set_orientation(
                Qt.Orientation.Vertical
            )  # Corrected: Use Qt.Orientation enum

            # Top panel - Data controls
            top_panel = QWidget()
            top_layout = QVBoxLayout(top_panel)

            # Data source selection
            self.data_source = QComboBox()
            self.data_source.add_items(["Vulnerabilities", "Scans", "Reports"])
            top_layout.add_widget(QLabel("Data Source:"))
            top_layout.add_widget(self.data_source)

            # Filter controls
            filter_layout = QHBoxLayout()
            self.filter_field = QComboBox()
            self.filter_field.add_items(["Severity", "Type", "Status"])
            self.filter_value = QLineEdit()
            self.filter_value.set_placeholder_text("Filter value...")
            self.apply_filter = QPushButton("Apply Filter")
            self.apply_filter.clicked.connect(self.apply_data_filter)
            filter_layout.add_widget(self.filter_field)
            filter_layout.add_widget(self.filter_value)
            filter_layout.add_widget(self.apply_filter)
            top_layout.add_layout(filter_layout)

            # Data table
            self.data_table = QTableWidget()
            self.data_table.set_column_count(4)
            self.data_table.set_horizontal_header_labels(
                ["ID", "Type", "Severity", "Status"]
            )
            top_layout.add_widget(self.data_table)

            # Bottom panel - Visualization and status
            bottom_panel = QWidget()
            bottom_layout = QVBoxLayout(bottom_panel)

            # Visualization controls
            vis_controls = QHBoxLayout()
            self.chart_type = QComboBox()
            self.chart_type.add_items(["Bar", "Line", "Pie"])
            self.generate_chart = QPushButton("Generate Chart")
            self.generate_chart.clicked.connect(self.generate_visualization)
            vis_controls.add_widget(QLabel("Chart Type:"))
            vis_controls.add_widget(self.chart_type)
            vis_controls.add_widget(self.generate_chart)
            bottom_layout.add_layout(vis_controls)

            # Status window
            self.status_window = QTextEdit()
            self.status_window.set_read_only(True)
            self.status_window.set_placeholder_text(
                "Analytics status will appear here..."
            )
            bottom_layout.add_widget(QLabel("Status:"))
            bottom_layout.add_widget(self.status_window)

            # Add panels to splitter
            splitter.add_widget(top_panel)
            splitter.add_widget(bottom_panel)

            main_layout.add_widget(splitter)
            self.set_layout(main_layout)

            def apply_data_filter(self):
                """Apply filter to the data."""
                field = self.filter_field.current_text()
                value = self.filter_value.text().strip()
                if value:
                    filtered_data = self.analytics.filter_data(field, value)
                    self.update_data_table(filtered_data)

                    def update_data_table(self, data):
                        """Update the data table with new information."""
                        self.data_table.set_row_count(len(data))
                        for row, item in enumerate(data):
                            self.data_table.set_item(
                                row, 0, QTableWidgetItem(str(item["id"]))
                            )
                            self.data_table.set_item(
                                row, 1, QTableWidgetItem(item["type"])
                            )
                            self.data_table.set_item(
                                row, 2, QTableWidgetItem(item["severity"])
                            )
                            self.data_table.set_item(
                                row, 3, QTableWidgetItem(item["status"])
                            )

                            def generate_visualization(self):
                                """Generate a data visualization."""
                                chart_type = self.chart_type.current_text()
                                self.analytics.generate_chart(chart_type)
                                self.status_window.append(
                                    f"Generated {chart_type} chart"
                                )

                                def update_status(self):
                                    """Update the status window with current analytics information."""
                                    status = self.analytics.get_status()
                                    self.status_window.append(status)

                                    def start_analytics(self):
                                        """Start the analytics session."""
                                        self.status_timer.start(1000)
                                        self.status_window.append(
                                            "Analytics session started"
                                        )

                                        def stop_analytics(self):
                                            """Stop the analytics session."""
                                            self.status_timer.stop()
                                            self.status_window.append(
                                                "Analytics session stopped"
                                            )
