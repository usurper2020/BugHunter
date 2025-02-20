"""
Analytics tab for the BugHunter application.

This tab provides tools for data analysis and visualization with real-time
status updates and interactive controls.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton, QSplitter, QProgressBar,
                           QComboBox, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import QTimer
from services.analytics_system import AnalyticsSystem

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
        splitter.setOrientation(1)  # Vertical split
        
        # Top panel - Data controls
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        # Data source selection
        self.data_source = QComboBox()
        self.data_source.addItems(["Vulnerabilities", "Scans", "Reports"])
        top_layout.addWidget(QLabel("Data Source:"))
        top_layout.addWidget(self.data_source)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        self.filter_field = QComboBox()
        self.filter_field.addItems(["Severity", "Type", "Status"])
        self.filter_value = QLineEdit()
        self.filter_value.setPlaceholderText("Filter value...")
        self.apply_filter = QPushButton("Apply Filter")
        self.apply_filter.clicked.connect(self.apply_data_filter)
        filter_layout.addWidget(self.filter_field)
        filter_layout.addWidget(self.filter_value)
        filter_layout.addWidget(self.apply_filter)
        top_layout.addLayout(filter_layout)
        
        # Data table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["ID", "Type", "Severity", "Status"])
        top_layout.addWidget(self.data_table)
        
        # Bottom panel - Visualization and status
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # Visualization controls
        vis_controls = QHBoxLayout()
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Bar", "Line", "Pie"])
        self.generate_chart = QPushButton("Generate Chart")
        self.generate_chart.clicked.connect(self.generate_visualization)
        vis_controls.addWidget(QLabel("Chart Type:"))
        vis_controls.addWidget(self.chart_type)
        vis_controls.addWidget(self.generate_chart)
        bottom_layout.addLayout(vis_controls)
        
        # Status window
        self.status_window = QTextEdit()
        self.status_window.setReadOnly(True)
        self.status_window.setPlaceholderText("Analytics status will appear here...")
        bottom_layout.addWidget(QLabel("Status:"))
        bottom_layout.addWidget(self.status_window)
        
        # Add panels to splitter
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def apply_data_filter(self):
        """Apply filter to the data."""
        field = self.filter_field.currentText()
        value = self.filter_value.text().strip()
        if value:
            filtered_data = self.analytics.filter_data(field, value)
            self.update_data_table(filtered_data)

    def update_data_table(self, data):
        """Update the data table with new information."""
        self.data_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.data_table.setItem(row, 1, QTableWidgetItem(item['type']))
            self.data_table.setItem(row, 2, QTableWidgetItem(item['severity']))
            self.data_table.setItem(row, 3, QTableWidgetItem(item['status']))

    def generate_visualization(self):
        """Generate a data visualization."""
        chart_type = self.chart_type.currentText()
        self.analytics.generate_chart(chart_type)
        self.status_window.append(f"Generated {chart_type} chart")

    def update_status(self):
        """Update the status window with current analytics information."""
        status = self.analytics.get_status()
        self.status_window.append(status)

    def start_analytics(self):
        """Start the analytics session."""
        self.status_timer.start(1000)
        self.status_window.append("Analytics session started")

    def stop_analytics(self):
        """Stop the analytics session."""
        self.status_timer.stop()
        self.status_window.append("Analytics session stopped")
