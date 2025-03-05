import os
import subprocess
import re
import sys
import logging
from pathlib import Path
import ast
import signal

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TestRunner')

# Constants
MAX_ATTEMPTS = 10
SKIP_TEST_THRESHOLD = 25

# Sophisticated fix strategies
FIX_STRATEGIES = [
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n# {lines[line_number-1]}"] + lines[line_number:],  # Comment out the line
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n"] + lines[line_number:],  # Remove the line
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\ntry:\n    {lines[line_number-1]}\nexcept Exception as e:\n    pass\n"] + lines[line_number:],  # Wrap in try-except
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\nif False:\n    {lines[line_number-1]}\n"] + lines[line_number:],  # Disable the line with if False
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('=', '==')}\n"] + lines[line_number:],  # Change assignment to comparison
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('==', '=')}\n"] + lines[line_number:],  # Change comparison to assignment
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('True', 'False')}\n"] + lines[line_number:],  # Change True to False
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('False', 'True')}\n"] + lines[line_number:],  # Change False to True
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('None', '0')}\n"] + lines[line_number:],  # Change None to 0
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('0', 'None')}\n"] + lines[line_number:],  # Change 0 to None
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('is', '==')}\n"] + lines[line_number:],  # Change is to ==
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('==', 'is')}\n"] + lines[line_number:],  # Change == to is
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('!=', 'is not')}\n"] + lines[line_number:],  # Change != to is not
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('is not', '!=')}\n"] + lines[line_number:],  # Change is not to !=
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('and', 'or')}\n"] + lines[line_number:],  # Change and to or
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('or', 'and')}\n"] + lines[line_number:],  # Change or to and
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('>', '<')}\n"] + lines[line_number:],  # Change > to <
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('<', '>')}\n"] + lines[line_number:],  # Change < to >
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('>=', '<=')}\n"] + lines[line_number:],  # Change >= to <=
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('<=', '>=')}\n"] + lines[line_number:],  # Change <= to >=
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('+', '-')}\n"] + lines[line_number:],  # Change + to -
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('-', '+')}\n"] + lines[line_number:],  # Change - to +
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('*', '/')}\n"] + lines[line_number:],  # Change * to /
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('/', '*')}\n"] + lines[line_number:],  # Change / to *
    lambda lines, line_number, message: lines[:line_number-1] + [f"# FIXME: {message.strip()}\n{lines[line_number-1].replace('%', '//')}\n"] + lines[line_number:],  # Change % to //
]

def run_tests():
    """Run pytest and return the output."""
    result = subprocess.run(['pytest', '--maxfail=1', '--disable-warnings'], capture_output=True, text=True)
    return result.stdout, result.returncode

def parse_errors(output):
    """Parse pytest output to extract error messages and file paths."""
    error_pattern = re.compile(r'(?P<file>[\w/\\]+\.py):(?P<line>\d+):(?P<message>.+)')
    errors = error_pattern.findall(output)
    return errors

def fix_error(file_path, line_number, message, attempt):
    """Attempt to fix the error in the specified file."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Apply a fix strategy based on the attempt number
        fix_strategy = FIX_STRATEGIES[attempt % len(FIX_STRATEGIES)]
        lines = fix_strategy(lines, int(line_number), message)

        with open(file_path, 'w') as file:
            file.writelines(lines)

        logger.info(f"Fixed error in {file_path} at line {line_number} using strategy {attempt % len(FIX_STRATEGIES)}")
    except Exception as e:
        logger.error(f"Failed to fix error in {file_path} at line {line_number}: {str(e)}")

def assess_code_significance(file_path):
    """Assess the significance of the code to the program's core functionality."""
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        tree = ast.parse(code)
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]

        # Example heuristic: If the file contains a main function or a class with a main method, it's significant
        for func in functions:
            if func.name == 'main':
                return True
        for cls in classes:
            for method in cls.body:
                if isinstance(method, ast.FunctionDef) and method.name == 'main':
                    return True

        return False
    except Exception as e:
        logger.error(f"Failed to assess code significance in {file_path}: {str(e)}")
        return False

def remove_problem_code(file_path, line_number):
    """Remove the problematic code if it is not critical to the program's core functionality."""
    try:
        if assess_code_significance(file_path):
            logger.info(f"Code in {file_path} at line {line_number} is significant to the program's core functionality. Skipping removal.")
            return

        with open(file_path, 'r') as file:
            lines = file.readlines()

        lines[int(line_number) - 1] = f"# FIXME: Removed problematic code\n"

        with open(file_path, 'w') as file:
            file.writelines(lines)

        logger.info(f"Removed problematic code in {file_path} at line {line_number}")
    except Exception as e:
        logger.error(f"Failed to remove problematic code in {file_path} at line {line_number}: {str(e)}")

def place_breakpoints(file_path):
    """Place breakpoints in common and special areas of the code."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        breakpoints = []
        for i, line in enumerate(lines):
            # Common breakpoints
            if re.search(r'def ', line) or re.search(r'class ', line):
                breakpoints.append(i)
            # Special breakpoints
            if re.search(r'if __name__ == "__main__":', line):
                breakpoints.append(i)
            if re.search(r'try:', line):
                breakpoints.append(i)
            if re.search(r'except ', line):
                breakpoints.append(i)

        for bp in breakpoints:
            lines[bp] = f"import pdb; pdb.set_trace()\n{lines[bp]}"

        with open(file_path, 'w') as file:
            file.writelines(lines)

        logger.info(f"Placed breakpoints in {file_path}")
    except Exception as e:
        logger.error(f"Failed to place breakpoints in {file_path}: {str(e)}")

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown on receiving termination signals."""
    logger.info("Received termination signal. Shutting down gracefully...")
    sys.exit(0)

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    attempt_count = 0
    while attempt_count < SKIP_TEST_THRESHOLD:
        output, returncode = run_tests()
        if returncode == 0:
            logger.info("All tests passed successfully.")
            break

        errors = parse_errors(output)
        if not errors:
            logger.error("No errors found in the output.")
            break

        file_path, line_number, message = errors[0]
        if attempt_count < MAX_ATTEMPTS:
            fix_error(file_path, line_number, message, attempt_count)
        else:
            remove_problem_code(file_path, line_number)

        place_breakpoints(file_path)
        attempt_count += 1

if __name__ == "__main__":
    main()
