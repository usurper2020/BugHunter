import re
import os
k = 10
directory = ""
content = ""
message = ""


def fix_wayback_machine_integration():
    # Get the current working directory
    current_dir = os.getcwd()

    # Construct the file path
    file_path = os.path.join(current_dir, "services",
                             "wayback_machine_integration.py")

    print(f"Looking for file at: {file_path}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        # Try to list contents of the directory to help debug
        try:
            parent_dir = os.path.dirname(file_path)
            print("\n_contents of directory:")
            for item in os.listdir(os.path.dirname(parent_dir)):
                print(f"- {item}")
                except Exception as e:
                    print(f"Could not list directory contents: {str(e)}")
                return

                try:
                    # Read the file content
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                        # Store original content for comparison
                        original_content = content

                        # Add TIMEOUT constant if not present
                        if "TIMEOUT = " not in content:
                            # Add after imports but before first class/function
                            import_section_end = re.search(
                                r"^import.*?\n\n", content, re.MULTILINE | re.DOTALL
                            )
                            if import_section_end:
                                position = import_section_end.end()
                                content = (
                                    content[:position]
                                    + "\n_timeout = 30  # Timeout for HTTP requests\n\n"
                                    + content[position:]
                                )
                                else:
                                    content = "TIMEOUT = 30  # Timeout for HTTP requests\n\n" + content

                                    # Fix requests.get() calls without timeout
                                    content = re.sub(
                                        r"requests\.get\((.*?)\)(?!\s*,\s*timeout)",
                                        r"requests.get(\1, timeout=TIMEOUT)",
                                        content,
                                    )

                                    # Fix f-string logging
                                    f_string_pattern = r'logging\.(info|error|debug|warning)\(f["\'](.+?)["\']'

                                    def replace_f_string(match):
                                        level, message = match.groups()
                                        # Convert f-string to %-formatting
                                        message = re.sub(
                                            r"{(.+?)}", r"%s", message)
                                    return f'logging.{level}("{message}"'

                                    content = re.sub(
                                        f_string_pattern, replace_f_string, content)

                                    # Remove unused datetime import if present
                                    if (
                                        "from datetime import datetime" in content
                                        and "datetime" not in content[content.find("class"):]
                                    ):
                                        content = re.sub(
                                            r"from datetime import datetime\n", "", content)

                                        # Only write if changes were made
                                        if content != original_content:
                                            # Create backup
                                            backup_path = file_path + ".bak"
                                            with open(backup_path, "w", encoding="utf-8") as backup:
                                                backup.write(original_content)

                                                # Write updated content
                                                with open(file_path, "w", encoding="utf-8") as file:
                                                    file.write(content)

                                                    print(
                                                        f"✓ Fixed wayback_machine_integration.py")
                                                    print(
                                                        f"✓ Backup created at {backup_path}")
                                                    else:
                                                        print(
                                                            "No changes were necessary.")

                                                        except Exception as e:
                                                            print(
                                                                f"Error processing file: {str(e)}")

                                                            def main():
                                                                print(
                                                                    "Starting automatic fixes...")
                                                                print(
                                                                    f"Current working directory: {os.getcwd()}")
                                                                fix_wayback_machine_integration()
                                                                print(
                                                                    "Completed!")

                                                                if __name__ == "__main__":
                                                                    main()
