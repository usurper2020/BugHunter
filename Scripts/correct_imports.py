import os
import re

def correct_imports(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Correct import statements
                content = re.sub(r'from services\.', 'from src.services.', content)
                content = re.sub(r'from utils\.', 'from src.utils.', content)
                content = re.sub(r'from tabs\.', 'from src.tabs.', content)
                content = re.sub(r'from config\.', 'from src.config.', content)
                content = re.sub(r'from db\.', 'from src.db.', content)
                content = re.sub(r'from gui\.', 'from src.gui.', content)
                content = re.sub(r'from nuclei\.', 'from src.nuclei.', content)
                content = re.sub(r'from ai\.', 'from src.ai.', content)
                
                with open(file_path, 'w') as f:
                    f.write(content)

if __name__ == "__main__":
    correct_imports('src')
    correct_imports('nuclei-templates')
    correct_imports('Scripts')
    correct_imports('tests')
    correct_imports('gui')
    correct_imports('ai')
    correct_imports('db')
    correct_imports('config')
    correct_imports('utils')
    correct_imports('tabs')
    correct_imports('services')
    correct_imports('nuclei')
