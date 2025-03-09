from .base_tab import BaseTab
from services.vulnerability_scanner import VulnerabilityScanner
from services.ai_system import AISystem
from typing import Dict
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
vulnerabilities = []
k = 10
prompt = ""
ai_system = None
message = ""
items = []
technologies = []
context = {}


"""
AI Chat tab implementation for the BugHunter application.
"""


class AIChatTab(QWidget):
        def __init__(self):
        super().__init__()
        self.init_ui()
        self.ai_system = AISystem()

        def init_ui(self):
            layout = QVBoxLayout()
            self.chat_history = QTextEdit()
            self.chat_history.set_read_only

            class AIChatTab(BaseTab):
                """AI Chat interface tab"""

                def __init__(
                    self,
                    ai_system: AISystem,
                    nuclei_scanner: VulnerabilityScanner = None,
                    parent=None,
                ):
                    self.ai_system = ai_system
                    self.nuclei_scanner = nuclei_scanner
                    super().__init__(parent)
                    if self.nuclei_scanner is None:
                        self.nuclei_scanner = VulnerabilityScanner(
                            self.ai_system.config_manager)

                        def _setup_ui(self):
                            """Setup the UI components"""
                            # Create chat history
                            self.chat_history = QTextEdit()
                            self.chat_history.set_read_only(True)
                            self.chat_history.set_placeholder_text(
                                "Chat history will appear here...")

                            # Add progress indicator
                            self.scan_status = QLabel("")
                            self.scan_progress = QProgressBar()
                            self.scan_progress.set_visible(False)

                            # Create target input area
                            target_widget = QWidget()
                            target_layout = QHBoxLayout()
                            target_widget.set_layout(target_layout)

                            self.target_input = QLineEdit()
                            self.target_input.set_placeholder_text(
                                "Enter target website URL...")
                            self.scan_button = QPushButton("Scan")
                            self.scan_button.clicked.connect(
                                self._initiate_scan)

                            target_layout.add_widget(QLabel("Target Website:"))
                            target_layout.add_widget(self.target_input)
                            target_layout.add_widget(self.scan_button)

                            # Create chat input area
                            input_widget = QWidget()
                            input_layout = QHBoxLayout()
                            input_widget.set_layout(input_layout)

                            self.input_field = QLineEdit()
                            self.input_field.set_placeholder_text(
                                "Type your message here...")
                            self.input_field.set_maximum_height(100)

                            self.send_button = QPushButton("Send")
                            self.send_button.clicked.connect(
                                self._send_message)
                            self.send_button.set_enabled(False)

                            # AI selection dropdown
                            self.ai_selector = QComboBox()
                            self.ai_selector.add_items(["OpenAI", "CodeGPT"])
                            self.ai_selector.current_index_changed.connect(
                                self._update_ai_system)

                            input_layout.add_widget(self.input_field)
                            input_layout.add_widget(self.send_button)
                            input_layout.add_widget(self.ai_selector)

                            # Add components to main layout
                            self.layout.add_widget(self.chat_history)
                            self.layout.add_widget(self.scan_status)
                            self.layout.add_widget(self.scan_progress)
                            self.layout.add_widget(target_widget)
                            self.layout.add_widget(input_widget)

                            # Add initial message
                            self._add_system_message(
                                "AI Assistant ready. Type your message and press Send."
                            )

                            """Setup the UI components"""
                            # Create chat history
                            self.chat_history = QTextEdit()
                            self.chat_history.set_read_only(True)
                            self.chat_history.set_placeholder_text(
                                "Chat history will appear here...")

                            # Add progress indicator
                            self.scan_status = QLabel("")
                            self.scan_progress = QProgressBar()
                            self.scan_progress.set_visible(False)

                            # Create target input area
                            target_widget = QWidget()
                            target_layout = QHBoxLayout()
                            target_widget.set_layout(target_layout)

                            self.target_input = QLineEdit()
                            self.target_input.set_placeholder_text(
                                "Enter target website URL...")
                            self.scan_button = QPushButton("Scan")
                            self.scan_button.clicked.connect(
                                self._initiate_scan)

                            target_layout.add_widget(QLabel("Target Website:"))
                            target_layout.add_widget(self.target_input)
                            target_layout.add_widget(self.scan_button)

                            # Create chat input area
                            input_widget = QWidget()
                            input_layout = QHBoxLayout()
                            input_widget.set_layout(input_layout)

                            self.input_field = QLineEdit()
                            self.input_field.set_placeholder_text(
                                "Type your message here...")
                            self.input_field.set_maximum_height(100)

                            self.send_button = QPushButton("Send")
                            self.send_button.clicked.connect(
                                self._send_message)
                            self.send_button.set_enabled(False)

                            # AI selection dropdown
                            self.ai_selector = QComboBox()
                            self.ai_selector.add_items(["OpenAI", "CodeGPT"])
                            self.ai_selector.current_index_changed.connect(
                                self._update_ai_system)

                            input_layout.add_widget(self.input_field)
                            input_layout.add_widget(self.send_button)
                            input_layout.add_widget(self.ai_selector)

                            # Add components to main layout
                            self.layout.add_widget(self.chat_history)
                            self.layout.add_widget(self.scan_status)
                            self.layout.add_widget(self.scan_progress)
                            self.layout.add_widget(target_widget)
                            self.layout.add_widget(input_widget)

                            # Add initial message
                            self._add_system_message(
                                "AI Assistant ready. Type your message and press Send."
                            )

                            def _update_ai_system(self):
                                """Update the AI system based on user selection"""
                                selected_ai = self.ai_selector.current_text()
                                if selected_ai == "OpenAI":
                                    self.ai_system.api_type = "openai"
                                    else:
                                        self.ai_system.api_type = "codegpt"
                                        self._add_system_message(
                                            f"Switched to {selected_ai} AI.")

                                        def _update_scan_progress(self, _status: str, _progress: int = None):
                                            """Update scan progress and status"""
                                            self.scan_status.set_text(status)
                                            if progress is not None:
                                                self.scan_progress.set_visible(
                                                    True)
                                                self.scan_progress.set_value(
                                                    progress)

                                                @pyqt_slot()
                                                def _send_message(self):
                                                    """Handle sending a message from the chat input."""
                                                    message = self.input_field.text().strip()
                                                    if not message:
                                                        QMessageBox.warning(
                                                            self, "Warning", "Message cannot be empty.")
                                                    return

                                                    self.chat_history.append(
                                                        f"You: {message}")
                                                    self.input_field.clear()

                                                    # Here you would typically call the AI system to get a response
                                                    response = self.ai_system.get_response(
                                                        message)  # Example call
                                                    self.chat_history.append(
                                                        f"AI: {response}")

                                                    """Handle sending a message from the chat input."""
                                                    message = self.input_field.text().strip()
                                                    if not message:
                                                        QMessageBox.warning(
                                                            self, "Warning", "Message cannot be empty.")
                                                    return

                                                    self.chat_history.append(
                                                        f"You: {message}")
                                                    self.input_field.clear()

                                                    # Here you would typically call the AI system to get a response
                                                    response = self.ai_system.get_response(
                                                        message)  # Example call
                                                    self.chat_history.append(
                                                        f"AI: {response}")

                                                    @pyqt_slot()
                                                    async def _initiate_scan(self):
                                                        """Initiate scan of target website"""
                                                        target = self.target_input.text().strip()
                                                        if not target:
                                                            self._add_system_message(
                                                                "Please enter a target website to scan.")
                                                        return

                                                        self._add_system_message(
                                                            f"Initiating scan of {target}...")
                                                        self.scan_progress.set_visible(
                                                            True)
                                                        self.scan_progress.set_value(
                                                            0)

                                                        try:
                                                                # Initial scan setup
                                                            self._update_scan_progress(
                                                                "Setting up scan...", 10)

                                                            if self.nuclei_scanner:
                                                                    # Start scanning
                                                                self._update_scan_progress(
                                                                    "Scanning target...", 30)
                                                                scan_results = await self.nuclei_scanner.scan_target(
                                                                    target, "quick_scan"
                                                                )

                                                                # Processing results
                                                                self._update_scan_progress(
                                                                    "Processing scan results...", 60)
                                                                self._add_system_message(
                                                                    "Scan complete. Analyzing results...")

                                                                # Generating insights
                                                                self._update_scan_progress(
                                                                    "Generating insights...", 80)
                                                                await self._generate_insights(target, scan_results)

                                                                # Complete
                                                                self._update_scan_progress(
                                                                    "Scan and analysis complete", 100)
                                                                self.scan_progress.set_visible(
                                                                    False)
                                                                else:
                                                                    self._add_system_message(
                                                                        "Nuclei scanner not available")
                                                                    self.scan_progress.set_visible(
                                                                        False)
                                                                    except Exception as e:
                                                                        self._add_system_message(
                                                                            f"Scan failed: {str(e)}")
                                                                        self.scan_progress.set_visible(
                                                                            False)

                                                                        async def _generate_insights(self, _target: str, _scan_results: Dict[str, _any]):
                                                                            """Generate enhanced bug bounty hunting insights for target with real-time updates"""
                                                                            try:
                                                                                    # Update progress
                                                                                self._update_scan_progress(
                                                                                    "Analyzing technology stack...", 40)
                                                                                tech_stack = await self.ai_system.analyze_tech_stack(str(scan_results))

                                                                                # Display detected technologies with confidence levels
                                                                                tech_info = [
                                                                                    f"{tech} ({data['confidence']*100:.0f}% confidence)"
                                                                                    for tech, data in tech_stack.items()
                                                                                    if data["detected"]
                                                                                ]
                                                                                if tech_info:
                                                                                    self._add_system_message(
                                                                                        f"Detected technologies: {', '.join(tech_info)}"
                                                                                    )

                                                                                    # Process vulnerabilities with progress updates
                                                                                    vulnerabilities = scan_results.get(
                                                                                        "vulnerabilities", [])
                                                                                    total_vulns = len(
                                                                                        vulnerabilities)

                                                                                    for idx, vuln in enumerate(vulnerabilities, 1):
                                                                                        progress = 40 + \
                                                                                            (40 * idx / total_vulns)
                                                                                        self._update_scan_progress(
                                                                                            f"Analyzing vulnerability {idx}/{total_vulns}...", int(
                                                                                            progress)
                                                                                        )

                                                                                        # Risk analysis
                                                                                        risk_data = await self.ai_system.analyze_vulnerability_risk(vuln)
                                                                                        self._add_system_message(
                                                                                            f"Risk Analysis for {vuln['type']}:")
                                                                                        self._add_ai_message(
                                                                                            risk_data["analysis"])

                                                                                        if risk_data["historical_context"]["similar_cases"] > 0:
                                                                                            self._add_system_message(
                                                                                                f"Historical Context: Found {risk_data['historical_context']['similar_cases']} similar cases\n"
                                                                                                f"Average Risk Score: {risk_data['historical_context']['average_risk']:.2f}\n"
                                                                                                f"Successful Exploits: {risk_data['historical_context']['successful_exploits']}"
                                                                                            )

                                                                                            # Generate safe PoC
                                                                                            self._add_system_message(
                                                                                                f"Generating proof of concept for {vuln['type']}..."
                                                                                            )
                                                                                            exploit = await self.ai_system.generate_exploit(vuln)
                                                                                            if exploit:
                                                                                                self._add_system_message(
                                                                                                    "Proof of Concept:")
                                                                                                self._add_ai_message(
                                                                                                    exploit)

                                                                                                # Add to learning data
                                                                                                self.ai_system.add_learning_data(
                                                                                                    {
                                                                                                    "target": target,
                                                                                                    "tech_stack": tech_stack,
                                                                                                    "scan_results": scan_results,
                                                                                                    "timestamp": datetime.now().isoformat(),
                                                                                                }
                                                                                                )

                                                                                                # Generate final report
                                                                                                self._update_scan_progress(
                                                                                                    "Generating comprehensive report...", 90)
                                                                                                prompt = self._create_comprehensive_prompt(
                                                                                                    target, tech_stack, scan_results)
                                                                                                final_report = await self.ai_system.get_response(prompt)
                                                                                                self._add_ai_message(
                                                                                                    final_report)

                                                                                                # Complete
                                                                                                self._update_scan_progress(
                                                                                                    "Analysis complete", 100)

                                                                                                except Exception as e:
                                                                                                    self._add_system_message(
                                                                                                        f"Error during analysis: {str(e)}")
                                                                                                    self._update_scan_progress(
                                                                                                        "Analysis failed", 0)
                                                                                                    self.scan_progress.set_visible(
                                                                                                        False)

                                                                                                    def _create_comprehensive_prompt(
                                                                                                        self, target: str, tech_stack: Dict[str, any], scan_results: Dict[str, any]
                                                                                                    ) -> str:
                                                                                                        """Create comprehensive analysis prompt"""
                                                                                                        prompt = (
                                                                                                            f"Provide detailed bug bounty hunting insights for {target} based on:\n"
                                                                                                        )
                                                                                                        prompt += f"\n_detected Technologies:"
                                                                                                        for tech, data in tech_stack.items():
                                                                                                                if data["detected"]:
                                                                                                                prompt += f"\n- {tech} ({data['confidence']*100:.0f}% confidence)"

                                                                                                                prompt += "\n\n_include in your analysis:"
                                                                                                                prompt += "\n1. Vulnerability Summary and Risk Assessment"
                                                                                                                prompt += "\n2. Technology-specific Attack Vectors"
                                                                                                                prompt += "\n3. Advanced Exploitation Techniques"
                                                                                                                prompt += "\n4. Business Impact Analysis"
                                                                                                                prompt += "\n5. Remediation Recommendations"
                                                                                                                prompt += "\n6. Similar Bug Bounty Reports"
                                                                                                                prompt += "\n7. Suggested Tools and Commands"
                                                                                                                prompt += "\n8. Additional Security Considerations"

                                                                                                            return prompt