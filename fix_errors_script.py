"""
Script to fix minor errors in the BugHunter application tests and enhance error handling.
"""


import os

# Step 1: Update src/config/__init__.py to expose the Config class and add error handling

init_file_path = 'src/config/__init__.py'
with open(init_file_path, 'a') as init_file:
    init_file.write('\nfrom .config import Config\n')  # Exposing Config class
    init_file.write('import logging\n')  # Import logging for error tracking


# Step 2: Update or create pytest.ini to set asyncio_default_fixture_loop_scope
pytest_ini_path = 'pytest.ini'
pytest_config = """
[pytest]
asyncio_default_fixture_loop_scope = function
# Additional pytest configurations can be added here
"""


if not os.path.exists(pytest_ini_path):  # Create pytest.ini if it doesn't exist

    with open(pytest_ini_path, 'w') as pytest_ini_file:  # Write default configuration

        pytest_ini_file.write(pytest_config)
else:
    with open(pytest_ini_path, 'a') as pytest_ini_file:  # Append configuration if it exists

        pytest_ini_file.write(pytest_config)

print("Fix script executed successfully. Please check for any errors in the logs.")
