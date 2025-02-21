import os
import re

def update_references(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update import statements
                    content = re.sub(r'from \.\.', 'from src', content)
                    content = re.sub(r'from \.', 'from src', content)
                    content = re.sub(r'from src.gui', 'from src.gui', content)
                    content = re.sub(r'from src.models', 'from src.models', content)
                    content = re.sub(r'from src.scanning', 'from src.scanning', content)
                    content = re.sub(r'from src.ai', 'from src.ai', content)
                    content = re.sub(r'from src.settings', 'from src.settings', content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_references("c:/Users/clabb/Desktop/BugHunter")
