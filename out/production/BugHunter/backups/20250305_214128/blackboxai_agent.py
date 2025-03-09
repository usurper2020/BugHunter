from rich.progress import Progress
from typing import Dict
from dataclasses import dataclass
import os
import ast
k = 10
directory = ""
message = ""
items = []
templates = []


@dataclass
   class BlackBoxAIAgent:
        def __init__(self, _project_root):
        self.project_root = project_root
        self.log_file = os.path.join(self.project_root, "error_report.txt")
        self.ignored_directories = {
            ".vscode",
            ".git",
            ".github",
            "__pycache__",
            "venv",
            ".venv",
            "nuclei-templates",
            "nuclei",
            "Nuclei",
        }
        self.good_files = {}  # Dictionary to store good files by directory
        self.bad_files = {}  # Dictionary to store bad files by directory

           def scan_project(self):
            """Scan the project directory for Python files and analyze them."""
            print("Scanning project for Python files...")
            python_files = self.get_python_files()
            total_files = len(python_files)
            print(f"Found {total_files} Python files.")

            # Use a progress bar to track progress
               with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Scanning files...", total=total_files)
                   for file_path in python_files:
                    self.analyze_file(file_path)
                    progress.update(task, advance=1)

                    # Write the report after scanning all files
                    self.write_report()
                    print(f"Scan complete. Report written to {self.log_file}")

                       def get_python_files(self):
                        """Retrieve all Python files in the project directory, excluding ignored directories."""
                        python_files = []
                           for root, dirs, files in os.walk(self.project_root):
                                # Skip ignored directories
                            dirs[:] = [
                                d for d in dirs if d not in self.ignored_directories]
                               for file in files:
                                    if file.endswith(".py"):
                                    python_files.append(
                                        os.path.join(root, file))
                                return python_files

                                   def analyze_file(self, _file_path):
                                    """Analyze a Python file for errors and log them."""
                                       try:
                                            with open(file_path, "r", encoding="utf-8") as file:
                                            source = file.read()
                                            # Parse the file into an Abstract Syntax Tree (AST)
                                            ast.parse(source)
                                            # If no errors, log the file as GOOD
                                            self.log_good(file_path)
                                               except SyntaxError as e:
                                                self.log_error(
                                                    file_path,
                                                    e,
                                                    "Syntax Error",
                                                    fix="Check for missing colons, parentheses, or invalid syntax.",
                                                )
                                                   except IndentationError as e:
                                                    self.log_error(
                                                        file_path,
                                                        e,
                                                        "Indentation Error",
                                                        fix="Ensure consistent indentation (e.g., 4 spaces per level).",
                                                    )
                                                       except Exception as e:
                                                            # Catch any other unexpected errors
                                                        self.log_error(
                                                            file_path,
                                                            e,
                                                            "Unknown Python Error",
                                                            fix="Manually review the file for potential issues.",
                                                        )

                                                        # Additional checks for circular imports
                                                        self.check_circular_imports(
                                                            file_path)

                                                           def check_circular_imports(self, _file_path):
                                                            """Check for circular imports in the file."""
                                                               try:
                                                                    with open(file_path, "r", encoding="utf-8") as file:
                                                                    source = file.read()
                                                                    tree = ast.parse(
                                                                        source)
                                                                    imports = [
                                                                        node.module
                                                                        for node in ast.walk(tree)
                                                                        if isinstance(node, ast.ImportFrom)
                                                                    ]
                                                                    # Check for circular imports (basic heuristic)
                                                                       for module in imports:
                                                                            if module and module in file_path:
                                                                            self.log_error(
                                                                                file_path,
                                                                                f"Circular import detected with module '{module}'",
                                                                                "Circular Import Error",
                                                                                fix="Refactor the code to remove circular dependencies.",
                                                                            )
                                                                               except Exception as e:
                                                                                self.log_error(
                                                                                    file_path, e, "Error during circular import check")

                                                                                   def log_error(self, _file_path, _error, _label, _fix=None):
                                                                                    """Log an error into the bad files dictionary."""
                                                                                    directory = os.path.dirname(
                                                                                        file_path)
                                                                                       if directory not in self.bad_files:
                                                                                        self.bad_files[directory] = [
                                                                                        ]
                                                                                        self.bad_files[directory].append(
                                                                                            {"file": file_path, "error": error, "label": label, "fix": fix}
                                                                                        )
                                                                                        print(
                                                                                            f"Logged error in {file_path}: {label}")

                                                                                           def log_good(self, _file_path):
                                                                                            """Log a GOOD message into the good files dictionary."""
                                                                                            directory = os.path.dirname(
                                                                                                file_path)
                                                                                               if directory not in self.good_files:
                                                                                                self.good_files[directory] = [
                                                                                                ]
                                                                                                self.good_files[directory].append(
                                                                                                    file_path)
                                                                                                print(
                                                                                                    f"File {file_path} is GOOD!")

                                                                                                   def write_report(self):
                                                                                                    """Write the report to a .txt file, separating good and bad files."""
                                                                                                       with open(self.log_file, "w", encoding="utf-8") as log:
                                                                                                        log.write(
                                                                                                            "Error Report\n")
                                                                                                        log.write(
                                                                                                            "=" * 50 + "\n\n")

                                                                                                        # Write GOOD files
                                                                                                        log.write(
                                                                                                            "GOOD FILES\n")
                                                                                                        log.write(
                                                                                                            "=" * 50 + "\n")
                                                                                                           for directory, files in self.good_files.items():
                                                                                                            log.write(
                                                                                                                f"Directory: {directory}\n")
                                                                                                               for file in files:
                                                                                                                log.write(
                                                                                                                    f"  - {file}\n")
                                                                                                                log.write(
                                                                                                                    "\n")

                                                                                                                # Write BAD files
                                                                                                                log.write(
                                                                                                                    "BAD FILES\n")
                                                                                                                log.write(
                                                                                                                    "=" * 50 + "\n")
                                                                                                                   for directory, errors in self.bad_files.items():
                                                                                                                    log.write(
                                                                                                                        f"Directory: {directory}\n")
                                                                                                                       for error in errors:
                                                                                                                        log.write(
                                                                                                                            f"  File: {error['file']}\n")
                                                                                                                        log.write(
                                                                                                                            f"  Error Type: {error['label']}\n")
                                                                                                                        log.write(
                                                                                                                            f"  Error Details: {error['error']}\n")
                                                                                                                           if hasattr(error["error"], "lineno"):
                                                                                                                            log.write(
                                                                                                                                f"  Line: {error['error'].lineno}\n")
                                                                                                                               if error["fix"]:
                                                                                                                                log.write(
                                                                                                                                    f"  Suggested Fix: {error['fix']}\n")
                                                                                                                                log.write(
                                                                                                                                    "-" * 50 + "\n")
                                                                                                                                log.write(
                                                                                                                                    "\n")

                                                                                                                                   def main():
                                                                                                                                        # Replace this with the root directory of your project
                                                                                                                                    project_root = r"C:\Users\clabb\Desktop\BugHunter"
                                                                                                                                    agent = BlackBoxAIAgent(
                                                                                                                                        project_root)
                                                                                                                                    agent.scan_project()

                                                                                                                                       if __name__ == "__main__":
                                                                                                                                        main()
