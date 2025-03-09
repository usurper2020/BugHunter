from typing import List

"""
Nuclei Analyzer for the BugHunter application.

This module provides functionality to run Nuclei scans and manage Nuclei templates.
"""

import json
import subprocess
from pathlib import Path


class NucleiAnalyzer:
    """
    Manages Nuclei scanning operations.
    """

    def __init__(self):
        # Breakpoint to verify initialization
        breakpoint()
        self.templates_dir = Path("nuclei-templates")
        self.results_dir = Path("data/scan_results")
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def scan(self, _targets: list) -> str:
        """
        Run a Nuclei scan on the specified targets.

            Args:
            targets (list): List of target URLs or IP addresses to scan.

            Returns:
            str: Scan results in JSON format.
            """
        try:
            # Breakpoint before running scan
            breakpoint()
            # Prepare Nuclei arguments
            args = ["nuclei", "-target", ",".join(targets), "-json", "-silent"]

            # Execute Nuclei scan
            result = subprocess.run(args, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Nuclei scan failed: {result.stderr}")

            # Parse JSON output
            vulnerabilities = []
            for line in result.stdout.splitlines():
                if line.strip():
                    try:
                        vuln = json.loads(line)
                        vulnerabilities.append(vuln)
                    except json.JSONDecodeError:
                        continue

            # Breakpoint after running scan
            breakpoint()
            return json.dumps(vulnerabilities, indent=4)

        except Exception as e:
            return f"Error: {str(e)}"

def some_function():
    # ...existing code...
    breakpoint()
    # ...existing code...
