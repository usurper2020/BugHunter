import subprocess

class Scanner:
    """
    Security scanner implementation for the BugHunter application.
    
    This class provides functionality to:
    - Execute security scans against specified targets
    - Use Nuclei as the underlying scanning engine
    - Handle scan execution and error management
    - Save scan results to output files
    """
    
    def __init__(self):
        """
        Initialize the Scanner instance.
        
        Sets up the scanner with default configuration.
        Future implementations may accept configuration parameters.
        """
        pass

    def run_scan(self, target):
        """
        Execute a security scan against the specified target.
        
        Uses Nuclei scanner to perform comprehensive security testing
        of the target, saving results to a file.
        
        Parameters:
            target (str): URL or IP address to scan
            
        Returns:
            str: Status message indicating scan result or error
            
        Raises:
            subprocess.CalledProcessError: If the scan process fails
            
        Note:
            Results are saved to 'results.txt' in the current directory
        """
        command = f"nuclei -u {target} -o results.txt"
        try:
            subprocess.run(command, shell=True, check=True)
            return "Scan completed successfully. Results saved to results.txt."
        except subprocess.CalledProcessError as e:
            return f"An error occurred while running the scan: {e}"
