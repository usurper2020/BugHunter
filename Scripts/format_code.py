import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Set, Tuple


class CodeFormatter:
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.temp_dir = Path(tempfile.mkdtemp())
        self.excluded_dirs: Set[str] = {
            "venv",
            ".venv",
            ".git",
            ".github",
            ".vscode",
            ".idea",
            ".pytest_cache",
            "faiss",
            "alembic",
            "Nuclei",
            "nuclei-templates",
            "Scripts",
            "__pycache__",
        }
        self.excluded_files: Set[str] = {".gitignore", ".pylintrc"}

    def is_excluded(self, path: Path) -> bool:
        """Check if path should be excluded"""
        # Check if any parent directory is in excluded dirs
        for parent in path.parents:
            if parent.name in self.excluded_dirs:
                return True

        # Check if file is in excluded files
        if path.name in self.excluded_files:
            return True

        return False

    def run_tools(self, file_path: Path) -> Dict[str, Tuple[int, str]]:
        """Run formatting tools and return their outputs"""
        results = {}

        # Run black
        try:
            black_output = subprocess.run(
                ["black", "--quiet", str(file_path)], capture_output=True, text=True
            )
            results["black"] = (black_output.returncode, black_output.stdout)
        except FileNotFoundError:
            results["black"] = (1, "Black not installed. Run: pip install black")

        # Run isort
        try:
            isort_output = subprocess.run(
                ["isort", str(file_path)], capture_output=True, text=True
            )
            results["isort"] = (isort_output.returncode, isort_output.stdout)
        except FileNotFoundError:
            results["isort"] = (1, "isort not installed. Run: pip install isort")

        # Run pylint
        try:
            pylint_output = subprocess.run(
                ["pylint", str(file_path)], capture_output=True, text=True
            )
            results["pylint"] = (pylint_output.returncode, pylint_output.stdout)
        except FileNotFoundError:
            results["pylint"] = (1, "Pylint not installed. Run: pip install pylint")

        return results

    def create_formatted_file(self, file_path: Path) -> Path:
        """Create a formatted version of the file in temp directory"""
        temp_file = self.temp_dir / file_path.name
        shutil.copy2(file_path, temp_file)

        # Apply formatting tools
        subprocess.run(["black", str(temp_file)], check=False)
        subprocess.run(["isort", str(temp_file)], check=False)

        return temp_file

    def get_python_files(self) -> List[Path]:
        """Get all Python files excluding specified directories and files"""
        python_files = []

        for file_path in self.target_path.rglob("*.py"):
            if not self.is_excluded(file_path):
                python_files.append(file_path)

        return python_files

    def process_files(self):
        """Process all Python files in the target directory"""
        try:
            python_files = self.get_python_files()

            if not python_files:
                print("No Python files found (excluding specified directories)")
                return

            print(f"Found {len(python_files)} Python files to process")

            for file_path in python_files:
                print(f"\nProcessing: {file_path}")

                # Run tools and get output
                results = self.run_tools(file_path)

                # Display results
                for tool, (returncode, output) in results.items():
                    print(f"\n{tool.upper()} Output:")
                    print(output if output else f"{tool} completed successfully")

                # Create formatted version
                formatted_file = self.create_formatted_file(file_path)

                # Show diff and ask for confirmation
                with open(file_path) as original, open(formatted_file) as formatted:
                    original_content = original.read()
                    formatted_content = formatted.read()

                if original_content != formatted_content:
                    print("\nChanges detected. Review the formatted version?")
                    if input("Show diff? (y/n): ").lower() == "y":
                        subprocess.run(["diff", str(file_path), str(formatted_file)])

                    if input("\nApply changes? (y/n): ").lower() == "y":
                        shutil.copy2(formatted_file, file_path)
                        print("Changes applied successfully!")
                    else:
                        print("Changes discarded.")
                else:
                    print("No formatting changes needed.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Cleanup temporary directory
            shutil.rmtree(self.temp_dir)


def main():
    print("Python Code Formatter")
    print("====================")
    print("Excluding: venv, .venv, .git, .github, .vscode, .idea, .pytest_cache,")
    print("          faiss, alembic, Nuclei, nuclei-templates, Scripts,")
    print("          __pycache__, .gitignore, .pylintrc")
    print("====================")

    # Get target directory
    target_dir = input(
        "Enter the target directory path (or '.' for current directory): "
    )
    target_dir = "." if not target_dir else target_dir

    # Verify tools installation
    required_tools = ["black", "isort", "pylint"]
    missing_tools = []

    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True)
        except FileNotFoundError:
            missing_tools.append(tool)

    if missing_tools:
        print("\nMissing required tools. Please install:")
        for tool in missing_tools:
            print(f"pip install {tool}")
        return

    # Initialize and run formatter
    formatter = CodeFormatter(target_dir)
    formatter.process_files()


if __name__ == "__main__":
    main()
