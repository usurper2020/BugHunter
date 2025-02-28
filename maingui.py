from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QTextEdit, QLineEdit




from PyQt6.QtCore import QSettings


import threading
from pathlib import Path
import sys
import queue
from datetime import datetime


class CodeAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Code Analyzer")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main frame
        self.main_frame = QWidget()
        self.setCentralWidget(self.main_frame)

        
        # Initialize settings
        self.settings = QSettings("BugHunter", "Theme")
        self.current_theme = self.settings.value("theme", "light")

        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        
        # Message queue for thread communication
        self.msg_queue = queue.Queue()
        
        # Create main frame
        # Message queue for thread communication
        self.msg_queue = queue.Queue()
        
        # Setup GUI components
        self.setup_gui()

        
        # Setup styles
        self.setup_styles()

        
        # Start message checking
        self.check_msg_queue()

    def setup_styles(self):
        """Setup application styles and themes"""
        # Load the appropriate theme
        theme_file = f"assets/styles/{self.current_theme}_theme.qss"
        try:
            with open(theme_file, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Theme file not found: {theme_file}")
            
        # Setup ttk styles
        style = ttk.Style()
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))


    def setup_gui(self):
        """Setup GUI components"""
        # File Selection
        self.setup_file_selection()
        
        # Progress and Status
        self.setup_progress_section()
        
        # Log Display
        self.setup_log_display()
        
        # Action Buttons
        self.setup_action_buttons()

    def setup_file_selection(self):
        """Setup file selection section"""
        # File selection label and button
        file_frame = QWidget(self.main_frame)
        file_layout = QHBoxLayout(file_frame)

        
        self.file_label = QLabel("Select Python File:")
        self.layout.addWidget(self.file_label)
        
        self.file_path = QLineEdit()
        self.layout.addWidget(self.file_path)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        self.layout.addWidget(browse_btn)



    def setup_progress_section(self):
        """Setup progress and status section"""
        progress_frame = QGroupBox("Progress", self.main_frame)
        progress_layout = QVBoxLayout(progress_frame)

        
        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)


    def setup_log_display(self):
        """Setup log display section"""
        log_frame = QGroupBox("Log", self.main_frame)
        log_layout = QVBoxLayout(log_frame)

        
        self.log_text = QTextEdit()
        self.layout.addWidget(self.log_text)

        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

    def setup_action_buttons(self):
        """Setup action buttons section"""
        button_frame = QWidget(self.main_frame)
        button_layout = QHBoxLayout(button_frame)

        
        # Add theme toggle button
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_btn)

        
        self.analyze_btn = QPushButton("Analyze Code")
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.layout.addWidget(self.analyze_btn)
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        self.layout.addWidget(clear_btn)


    def browse_file(self):
        """Open file browser dialog"""
        filename, _ = QFileDialog.getOpenFileName(self, "Select Python File", "", "Python files (*.py);;All files (*)")
        if filename:
            self.file_path.setText(filename)
            self.log_message(f"Selected file: {filename}")


    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")


    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")

    def start_analysis(self):
        """Start the code analysis in a separate thread"""
        if not self.file_path.text():
            self.log_message("Error: No file selected!")
            return
        
        self.analyze_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Start analysis thread
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()


    def run_analysis(self):
        """Run the code analysis"""
        try:
            self.msg_queue.put(('status', "Initializing analysis..."))
            self.msg_queue.put(('progress', 10))
            
            analyzer = CodeAnalyzer(self.file_path.get())
            
            self.msg_queue.put(('status', "Parsing file..."))
            self.msg_queue.put(('progress', 30))
            analyzer.parse_file()
            
            self.msg_queue.put(('status', "Analyzing code..."))
            self.msg_queue.put(('progress', 50))
            analyzer.analyze_code()
            
            self.msg_queue.put(('status', "Creating module structure..."))
            self.msg_queue.put(('progress', 70))
            analyzer.create_module_structure()
            
            self.msg_queue.put(('progress', 100))
            self.msg_queue.put(('status', "Analysis complete!"))
            self.msg_queue.put(('log', f"Code has been modularized and saved in: {analyzer.output_dir}"))
            
        except Exception as e:
            self.msg_queue.put(('error', f"Error during analysis: {str(e)}"))
        finally:
            self.msg_queue.put(('enable_button', None))

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.settings.setValue("theme", self.current_theme)
        self.setup_styles()

    def check_msg_queue(self):
        """Check for messages from the analysis thread"""
        try:
            while True:

                msg_type, msg_content = self.msg_queue.get_nowait()
                
                if msg_type == 'status':
                    self.status_label['text'] = msg_content
                elif msg_type == 'progress':
                    self.progress_bar['value'] = msg_content
                elif msg_type == 'log':
                    self.log_message(msg_content)
                elif msg_type == 'error':
                    self.log_message(f"ERROR: {msg_content}")
                    self.status_label['text'] = "Error occurred"
                elif msg_type == 'enable_button':
                    self.analyze_btn.state(['!disabled'])
                
        except queue.Empty:
            pass
        finally:
            # Schedule next check
            self.root.after(100, self.check_msg_queue)

def main():
    app = QApplication(sys.argv)
    window = CodeAnalyzerGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
