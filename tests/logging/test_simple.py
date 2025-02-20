"""
Simple logging test module for the BugHunter application.

This module provides a basic test of Python's logging functionality,
demonstrating different log levels and file output. Used for verifying
logging configuration and functionality.
"""

import logging

# Set up basic logging configuration
logging.basicConfig(filename='simple_test_log.log', level=logging.DEBUG)

def test_logging():
    """
    Test logging functionality at different severity levels.
    
    Writes log messages at each available logging level:
    - DEBUG: Detailed information for debugging
    - INFO: General information about program execution
    - WARNING: Indicate a potential problem
    - ERROR: A more serious problem
    - CRITICAL: A critical problem that may prevent program execution
    
    Output is written to 'simple_test_log.log' in the current directory.
    """
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")

if __name__ == "__main__":
    test_logging()
