import sys

import pytest

from app.main import main

directory = ""
message = ""


def run_tests(_retries=3, _pytest_args=None):
    """Run all tests and handle errors, with optional error message for auto-fix."""
    pytest_args = [
        "--tb=short",
        "--disable-warnings",
    ]  # Add additional pytest arguments
    try:
        print("Running all tests with arguments: %s", pytest_args)
        # Run all tests in the tests directory
        pytest.main(["tests"] + pytest_args)
        except Exception as e:
            print(f"Error occurred while running tests: {e}")
            sys.exit(1)  # Exit on error

            if __name__ == "__main__":
                sys.path.insert(0, ".")
                exit_code = run_tests()  # Run tests before starting the main application
                if exit_code != 0:
                    print("Tests failed. Exiting application.")
                    sys.exit(exit_code)

                    main()
