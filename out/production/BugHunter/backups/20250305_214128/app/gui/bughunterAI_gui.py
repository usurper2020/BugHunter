from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
vulnerabilities = []
url = ""
k = 10
message = ""


class templates = []


ScannerThread(QThread):
    update_signal = pyqt_signal(str)

    def __init__(self, _scanner, _url):
        super().__init__()
        self.scanner = scanner
        self.url = url

        def run(self):
            vulnerabilities = self.scanner.scan_website(self.url)
            for vuln in vulnerabilities:
                self.update_signal.emit(
                    f"Vulnerability found: {vuln['name']} (Severity: {vuln['severity']})"
                )

                class MainWindow(QMainWindow):
                    def __init__(self, _scanner):
                        super().__init__()
                        self.scanner = scanner
                        self.set_window_title("Vulnerability Scanner")
                        self.set_geometry(100, 100, 600, 400)

                        layout = QVBoxLayout()
                        self.text_edit = QTextEdit()
                        self.scan_button = QPushButton("Start Scan")
                        self.scan_button.clicked.connect(self.start_scan)

                        layout.add_widget(self.text_edit)
                        layout.add_widget(self.scan_button)

                        container = QWidget()
                        container.set_layout(layout)
                        self.set_central_widget(container)

                        def start_scan(self):
                            url = "http://example.com"  # Replace with user input or predefined URL
                            self.scanner_thread = ScannerThread(
                                self.scanner, url)
                            self.scanner_thread.update_signal.connect(
                                self.update_results)
                            self.scanner_thread.start()

                            def update_results(self, _message):
                                self.text_edit.append(message)

                                def main():
                                    app = QApplication([])
                                    kb = NucleiKnowledgeBase()
                                    kb.load_templates(
                                        "/path/to/nuclei-templates")
                                    kb.create_vector_db()
                                    scanner = WebsiteScanner(kb)
                                    window = MainWindow(scanner)
                                    window.show()
                                    app.exec()

                                    if __name__ == "__main__":
                                        main()
