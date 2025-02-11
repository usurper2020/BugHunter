import subprocess

class Scanner:
    def __init__(self):
        pass

    def run_scan(self, target):
        # Example using Nuclei for scanning
        command = f"nuclei -u {target} -o results.txt"
        try:
            subprocess.run(command, shell=True, check=True)
            return "Scan completed successfully. Results saved to results.txt."
        except subprocess.CalledProcessError as e:
            return f"An error occurred while running the scan: {e}"
