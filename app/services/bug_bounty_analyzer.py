from .nuclei_analyzer import NucleiAnalyzer
from .ai_system import AISystem
from typing import Dict, Optional
import json
from typing import Optional
vulnerabilities = []
k = 10
prompt = ""
ai_system = None
suggestions = []

"""
Bug Bounty Analyzer for the BugHunter application.

This module provides functionality to combine Nuclei scanning with AI analysis.
"""

class BugBountyAnalyzer:
    """
    Combines Nuclei scanning with AI analysis for bug bounty hunting.
    """

    def __init__(self, _ai_system: AISystem, _nuclei_analyzer: NucleiAnalyzer):
        self.ai_system = ai_system
        self.nuclei_analyzer = nuclei_analyzer
        # Breakpoint to verify initialization
        breakpoint()

    def analyze_target(self, _target: str, _detail_level: str = "basic") -> Dict:
        """
        Analyze a target with optional AI insights.

        Args:
            target: The target URL or IP address
            detail_level: 'basic' or 'detailed' analysis

        Returns:
            Dict containing scan results and AI insights
        """
        # Breakpoint before analyzing target
        breakpoint()
        # Run Nuclei scan
        scan_results = self.nuclei_analyzer.scan([target])

        # Only get AI insights if user requests them
        ai_insights = None
        if detail_level in ["basic", "detailed"]:
            ai_insights = self.get_scan_insights(
                scan_results, detail_level)

        # Breakpoint after analyzing target
        breakpoint()
        return {"scan_results": scan_results, "ai_insights": ai_insights}

    def get_scan_insights(
        self, _scan_results: Dict, _detail_level: str
    ) -> Optional[str]:
        """
        Get AI analysis of scan results.

        Args:
            scan_results: Results from Nuclei scan
            detail_level: 'basic' or 'detailed' analysis

        Returns:
            AI-generated insights as string
        """
        prompt = self._create_analysis_prompt(
            scan_results, detail_level)
        return self.ai_system.get_response(prompt)

    def _create_analysis_prompt(self, _scan_results: Dict, _detail_level: str) -> str:
        """
        Create prompt for AI analysis based on scan results.

        Args:
            scan_results: Results from Nuclei scan
            detail_level: 'basic' or 'detailed' analysis

        Returns:
            Formatted prompt string
        """
        if detail_level == "basic":
            return (
                f"Provide a brief overview of these security scan results:\n"
                f"{json.dumps(scan_results, indent=2)}\n"
                f"Focus on the most critical vulnerabilities."
            )
        else:
            return (
                f"Provide a detailed analysis of these security scan results:\n"
                f"{json.dumps(scan_results, indent=2)}\n"
                f"Include:\n"
                f"- Vulnerability descriptions\n"
                f"- Potential impact\n"
                f"- Remediation suggestions\n"
                f"- Risk assessment"
            )

    def analyze(self, data: str) -> str:
        # Method implementation
        return data