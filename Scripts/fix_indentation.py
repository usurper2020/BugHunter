import os
import re


def fix_indentation_issues(file_path):
    """Fix indentation issues in a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Remove any mixed tabs and spaces
        lines = content.splitlines()
        fixed_lines = []

        for line in lines:
            # Convert tabs to spaces (4 spaces per tab)
            fixed_line = line.replace("\t", "    ")

            # Remove trailing whitespace
            fixed_line = fixed_line.rstrip()

            # Fix common indentation issues
            if fixed_line.strip():  # If line is not empty
                # Count leading spaces
                leading_spaces = len(fixed_line) - len(fixed_line.lstrip())
                # Ensure indentation is multiple of 4
                correct_spaces = (leading_spaces // 4) * 4
                fixed_line = " " * correct_spaces + fixed_line.lstrip()

            fixed_lines.append(fixed_line)

        # Write back the fixed content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(fixed_lines))

        print(f"Fixed indentation in: {file_path}")
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False


def process_directory(directory):
    """Process all Python files in a directory recursively."""
    fixed_count = 0
    error_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if fix_indentation_issues(file_path):
                    fixed_count += 1
                else:
                    error_count += 1

    return fixed_count, error_count


def main():
    # Directory containing your Python files
    project_dir = "C:\\Users\\clabb\\Desktop\\BugHunter\\app"

    print("Starting indentation fix process...")
    fixed, errors = process_directory(project_dir)

    print("\nSummary:")
    print(f"Files processed successfully: {fixed}")
    print(f"Files with errors: {errors}")
    print("\nNext steps:")
    print("1. Run 'black' to format your code:")
    print("   pip install black")
    print("   black .")
    print("2. Run 'pylint' again to check for remaining issues:")
    print("   pylint app/")


if __name__ == "__main__":
    main()
