import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
from pathlib import Path
import sys
import queue
from datetime import datetime
from code_analyzer import CodeAnalyzer  # Import CodeAnalyzer from the appropriate module

class CodeAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Analyzer")
        self.root.geometry("800x600")
        
        # Message queue for thread communication
        self.msg_queue = queue.Queue()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.setup_gui()
        self.setup_styles()
        
        # Start message checking
        self.check_msg_queue()

    def setup_styles(self):
        """Setup ttk styles"""
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
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky="we", pady=5)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.file_entry.grid(row=0, column=0, padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=1, padx=5)

    def setup_progress_section(self):
        """Setup progress and status section"""
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="5")
        progress_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky="we", pady=5)

    def setup_log_display(self):
        """Setup log display section"""
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

    def setup_action_buttons(self):
        """Setup action buttons section"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.analyze_btn = ttk.Button(button_frame, text="Analyze Code", command=self.start_analysis)
        self.analyze_btn.grid(row=0, column=0, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=0, column=1, padx=5)

    def browse_file(self):
        """Open file browser dialog"""
        filename = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.log_message(f"Selected file: {filename}")

    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")

    def start_analysis(self):
        """Start the code analysis in a separate thread"""
        if not self.file_path.get():
            self.log_message("Error: No file selected!")
            return
        
        self.analyze_btn.state(['disabled'])
        self.progress_bar['value'] = 0
        
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
    root = tk.Tk()
    app = CodeAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()