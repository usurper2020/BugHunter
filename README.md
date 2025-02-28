# BugHunter Testing Guide

## Overview

This document provides instructions on how to run tests for the BugHunter project, interpret the results, and fix any errors that may arise.

## Running Tests

To run the tests, use the following command:

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

### Coverage Reporting

- The `--cov=.` option specifies that coverage should be measured for the entire project.
- The `--cov-report=term-missing` option will show which lines are not covered in the terminal.
- The `--cov-report=html` option generates an HTML report for a visual representation of coverage.

## Interpreting Results

- If tests fail, pytest will provide detailed output, including the file name and line number where the error occurred.
- Use the `--tb=long` option for detailed traceback information.

## Fixing Errors

1. **Identify the Error**: Review the output from pytest to understand what went wrong.
2. **Locate the Code**: Use the file name and line number provided in the error message to find the relevant code.
3. **Make Corrections**: Update the code as necessary to fix the issue.
4. **Re-run Tests**: After making changes, run the tests again to check for any remaining errors.

## Additional Tools

Consider using the following plugins to enhance your testing experience:

- **pytest-flake8**: Integrates flake8 checks into your pytest runs.
- **pytest-pylint**: Integrates pylint checks to catch potential errors.

## Using the Tests

To run the tests, simply execute the following command in your terminal:

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

This command will run all tests in the project, measure coverage, and generate a report.

## Auto-Fixing Errors

To automate the process of fixing errors and rerunning tests until a file reaches 100% coverage, you can use the following approach:

1. **Use a Linter**: Integrate a linter like `flake8` or `pylint` to catch style and syntax errors.
2. **Create a Script**: Write a script that:
   - Runs the tests.
   - Checks the coverage report.
   - If coverage is below 100%, it will log the errors and attempt to fix them (you may need to implement specific logic for fixing).
   - Reruns the tests until coverage is 100% or no more errors are found.

3. **Example Script**:
   You can create a simple Python script to automate this process. Here’s a basic example:

   ```python
   import subprocess
   import sys
   import os

   def run_tests():
       result = subprocess.run(
           [sys.executable, '-m', 'pytest', '--cov=.', '--cov-report=term-missing'],
           capture_output=True,
           text=True
       )
       return result.returncode

   def main():
       while True:
           exit_code = run_tests()
           if exit_code != 0:
               print("Errors found. Attempting to fix...")
               # Implement your auto-fix logic here
           else:
               print("All tests passed with 100% coverage!")
               break

   if __name__ == "__main__":
       main()
   ```

## Running the `run_tests.py` Script

To run the `run_tests.py` script, use the following command in your terminal:

```bash
python run_tests.py
```

**Important**: Ensure that there are no trailing backslashes or additional characters in the command. For example, avoid using:

```bash
python run_tests.py\
```

This command will execute the script, run the tests, and attempt to fix any errors automatically.

To run the `run_tests.py` script, use the following command in your terminal:

```bash
python run_tests.py
```

**Important**: Ensure that there are no trailing backslashes or additional characters in the command. This command will execute the script, run the tests, and attempt to fix any errors automatically.

### Script Functionality

- The script will run all tests in the project and check for coverage.
- If errors are found, it will log the details and reference related files for context.
- The script will attempt to fix errors automatically and prompt for manual fixes if necessary.

## Conclusion

By following this guide, you can effectively run tests, identify issues, and ensure that your code meets the required coverage standards. The auto-fixing setup will help streamline the process of achieving 100% coverage.
