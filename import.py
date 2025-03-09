import os
import re

def replace_imports_in_file(file_path):
    """
    Replaces all import statements starting with 'src.' to 'app.' in a given file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace all occurrences of 'src.' with 'app.' in import statements
    updated_content = re.sub(r'\bfrom src\.', 'from app.', content)
    updated_content = re.sub(r'\bimport src\.', 'import app.', updated_content)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def process_project_folder(project_folder):
    """
    Recursively processes all files in the project folder, replacing 'src.' with 'app.' in imports.
    """
    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith('.py'):  # Only process Python files
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                replace_imports_in_file(file_path)


if __name__ == "__main__":
    # Define the path to your project folder
    project_folder = r"C:\Users\clabb\Desktop\BugHunter"

    # Process the project folder
    process_project_folder(project_folder)

    print("Finished replacing 'src.' with 'app.' in all Python files.")