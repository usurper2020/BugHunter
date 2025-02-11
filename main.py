import sys
import logging
import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QMessageBox, QTextEdit, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt
from dotenv import load_dotenv
from openai import OpenAI
import requests

# Configure logging first
def configure_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"bughunter_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )
    return logging.getLogger('BugHunter.Main')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize logger first
        self.logger = logging.getLogger('BugHunter.MainWindow')
        self.logger.info("Initializing MainWindow")
        
        # Initialize variables
        self.openai_client = None
        self.codegpt_client = None
        
        # Setup UI first
        self.init_ui()
        
        # Then initialize APIs
        self.init_apis()

    def init_ui(self):
        self.logger.info("Setting up UI")
        self.setWindowTitle('BugHunter')
        self.setMinimumSize(800, 600)

        # Create and set central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Setup tabs
        self.setup_tabs()
        
        self.logger.info("UI setup completed")

    def init_apis(self):
        self.logger.info("Initializing APIs")
        try:
            # Create .env file if it doesn't exist
            env_path = Path('.env')
            if not env_path.exists():
                template = (
                    "OPENAI_API_KEY=your_openai_api_key_here\n"
                    "CODEGPT_API_KEY=your_codegpt_api_key_here\n"
                )
                env_path.write_text(template)
                QMessageBox.warning(
                    self,
                    "Environment Setup",
                    "A template .env file has been created. Please add your API keys."
                )
                return

            # Load environment variables
            load_dotenv(override=True)
            
            # Initialize OpenAI client
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                try:
                    self.openai_client = OpenAI(api_key=openai_key)
                    self.logger.info("OpenAI client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize OpenAI client: {e}")
            
            # Initialize CodeGPT client
            codegpt_key = os.getenv('CODEGPT_API_KEY')
            if codegpt_key and codegpt_key != 'your_codegpt_api_key_here':
                try:
                    self.codegpt_client = CodeGPTClient(codegpt_key)
                    self.logger.info("CodeGPT client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize CodeGPT client: {e}")

        except Exception as e:
            self.logger.error(f"Failed to initialize API clients: {e}")
            QMessageBox.warning(
                self,
                "Setup Warning",
                f"Failed to initialize API clients: {str(e)}"
            )

    def setup_tabs(self):
        self.logger.info("Setting up tabs")
        # Create AI Chat tab
        ai_chat_tab = AIChatTab(
            openai_client=self.openai_client,
            codegpt_client=self.codegpt_client
        )
        self.tab_widget.addTab(ai_chat_tab, "AI Chat")
        
        # Add placeholder tabs
        self.tab_widget.addTab(QWidget(), "Scanner")
        self.tab_widget.addTab(QWidget(), "Tools")
        self.tab_widget.addTab(QWidget(), "Amass")
        self.tab_widget.addTab(QWidget(), "Nuclei")
        
        self.logger.info("Tabs setup completed")

class AIChatTab(QWidget):
    def __init__(self, openai_client=None, codegpt_client=None):
        super().__init__()
        self.logger = logging.getLogger('BugHunter.AIChatTab')
        self.openai_client = openai_client
        self.codegpt_client = codegpt_client
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # API Selection
        self.api_selector = QComboBox()
        self.api_selector.addItems(['OpenAI', 'CodeGPT'])
        layout.addWidget(self.api_selector)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Input field
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)

    def send_message(self):
        # Implementation of send_message method
        pass

def main():
    # Create application instance
    app = QApplication(sys.argv)
    
    # Configure logging
    logger = configure_logging()
    logger.info("Starting BugHunter application")
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        logger.info("Main window displayed")
        
        # Start event loop
        return app.exec()
        
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
