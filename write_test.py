"""
File writing permission test for the BugHunter application.

This script attempts to create a test file to verify that the application
has proper permissions to write files in the current directory. This is
crucial for features that need to save output, logs, or configuration.
"""

def test_file_writing():
    """
    Test file writing capabilities.
    
    Creates a test file with simple content to verify that:
    1. The application has write permissions
    2. File creation works correctly
    3. File writing operations succeed
    
    The test file is created as 'test_output.txt' in the
    current working directory.
    
    Note:
        Success is indicated by the presence of the output file
        with the expected content after execution.
    """
    with open('test_output.txt', 'w') as f:
        f.write("This is a test output file to verify writing permissions.\n")
        f.write("If this file is created successfully, then writing to files is working.\n")

if __name__ == '__main__':
    test_file_writing()
