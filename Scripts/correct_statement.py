import re
import os
k = 10
content = ""


def templates = []


correct_statements(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                with open(file_path, "r") as f:
                    content = f.read()

                    # Correct specific statements if needed
                    # Example: Replace old function calls with new ones
                    content = re.sub(r"old_function\(",
                                     "new_function(", content)

                    with open(file_path, "w") as f:
                        f.write(content)

                        if __name__ == "__main__":
                            correct_statements("src")
                            correct_statements("nuclei-templates")
                            correct_statements("Scripts")
