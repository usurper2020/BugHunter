import ast
import os
import black 
import docstring_parser
import importlib
import importlib.metadata
import importlib.metadata as metadata
import importlib.metadata as metadata
import unittest
from typing import Set, Dict, List, Any
import importlib.metadata
import importlib.metadata
from pathlib import Path

class CodeAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tree = None
        self.dependencies = set()
        self.imports = []
        self.classes = []
        self.functions = []
        self.doc_strings = {}
        self.output_dir = Path()

    def parse_file(self) -> None:
        """Parse the Python file and create AST."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.tree = ast.parse(content)
        except Exception as e:
            raise ValueError(f"Error parsing file: {str(e)}")

    def analyze_dependencies(self, node: ast.AST) -> Set[str]:
        """
        Analyze dependencies between components and external libraries.
        """
        dependencies = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Import):
                for name in child.names:
                    dependencies.add(name.name.split('.')[0])
            elif isinstance(child, ast.ImportFrom):
                if child.module:
                    dependencies.add(child.module.split('.')[0])
        return dependencies

    def extract_docstring(self, node: ast.AST) -> str:
        """Extract and parse docstring from node."""
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node) or ""
        else:
            docstring = ""
        return docstring_parser.parse(docstring)

    def analyze_code(self) -> None:
        """Analyze and categorize code components."""
        if self.tree is None:
            raise ValueError("AST tree is not initialized. Please call parse_file() first.")
        for node in ast.walk(self.tree):
            parent_map = {child: parent for parent in ast.walk(self.tree) for child in ast.iter_child_nodes(parent)}
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self.imports.append(ast.unparse(node))
                self.dependencies.update(self.analyze_dependencies(node))
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'code': ast.unparse(node),
                    'docstring': self.extract_docstring(node),
                    'methods': self.extract_methods(node),
                    'dependencies': self.analyze_dependencies(node)
                }
            elif isinstance(node, ast.FunctionDef):
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.iter_child_nodes(self.tree) if isinstance(parent, ast.ClassDef)):  # Standalone functions only
                    func_info = {
                        'name': node.name,
                        'code': ast.unparse(node),
                        'docstring': self.extract_docstring(node),
                        'dependencies': self.analyze_dependencies(node)
                    }
                    self.functions.append(func_info)
                
                if not isinstance(parent_map.get(node), ast.ClassDef):  # Standalone functions only
                    func_info = {
                        'name': node.name,
                        'code': ast.unparse(node),
                        'docstring': self.extract_docstring(node),
                        'dependencies': self.analyze_dependencies(node)
                    }
                    self.functions.append(func_info)

    def extract_methods(self, class_node: ast.ClassDef) -> List[Dict[str, Any]]:
        """Extract methods from a class definition."""
        methods = []
        for node in ast.iter_child_nodes(class_node):
            if isinstance(node, ast.FunctionDef):
                method_info = {
                    'name': node.name,
                    'code': ast.unparse(node),
                    'docstring': self.extract_docstring(node)
                }
                methods.append(method_info)
        return methods

    def format_code(self, code: str) -> str:
        """Format code using black."""
        try:
            return black.format_str(code, mode=black.FileMode())
        except Exception:
            return code  # Return original code if formatting fails

    def generate_test_file(self, component_name: str, component_type: str) -> str:
        """Generate a test file template for a component."""
        test_template = f"""import unittest
from ..{component_type} import {component_name}

class Test{component_name}(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_{component_name.lower()}_creation(self):
        # TODO: Implement test
        pass

if __name__ == '__main__':
    unittest.main()
"""
        return self.format_code(test_template)

    def create_module_structure(self) -> None:
        """Create the modular structure and write files."""
        # Create output directory
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.output_dir = Path(f"{base_name}_modules")
        self.output_dir.mkdir(exist_ok=True)

        # Create directory structure
        (self.output_dir / 'tests').mkdir(exist_ok=True)
        (self.output_dir / 'docs').mkdir(exist_ok=True)

        # Write files
        self._write_init_file()
        self._write_dependencies_file()
        self._write_requirements_file()
        self._write_classes()
        self._write_functions()
        self._write_main_file()
        self._write_documentation()
        self._write_setup_file()

    def _write_init_file(self) -> None:
        """Write the __init__.py file."""
        init_content = "# Generated module initialization\n"
        (self.output_dir / '__init__.py').write_text(self.format_code(init_content))

    def _write_dependencies_file(self) -> None:
        """Write the dependencies.py file."""
        if self.imports:
            content = '\n'.join(self.imports)
            (self.output_dir / 'dependencies.py').write_text(self.format_code(content))

    def _write_requirements_file(self) -> None:
        """Write requirements.txt with version information."""
        requirements = []
        for dep in self.dependencies:
            try:
                version = pkg_resources.get_distribution(dep).version
                requirements.append(f'{dep}=={version}')
            except pkg_resources.DistributionNotFound:
                requirements.append(dep)
        
        (self.output_dir / 'requirements.txt').write_text('\n'.join(requirements))

    def _write_classes(self) -> None:
        """Write class files and their corresponding tests."""
        for class_info in self.classes:
            # Write class file
            class_content = f'from .dependencies import *\n\n{class_info["code"]}'
            class_file = self.output_dir / f"{class_info['name'].lower()}.py"
            class_file.write_text(self.format_code(class_content))

            # Write test file
            test_content = self.generate_test_file(class_info['name'], 'classes')
            test_file = self.output_dir / 'tests' / f"test_{class_info['name'].lower()}.py"
            test_file.write_text(test_content)

    def _write_functions(self) -> None:
        """Write functions file and tests."""
        if self.functions:
            # Write functions file
            func_content = 'from .dependencies import *\n\n'
            func_content += '\n\n'.join(f"{func['code']}" for func in self.functions)
            (self.output_dir / 'functions.py').write_text(self.format_code(func_content))

            # Write test file for functions
            test_content = "import unittest\nfrom ..functions import *\n\n"
            test_content += "class TestFunctions(unittest.TestCase):\n"
            for func in self.functions:
                test_content += f"""
    def test_{func['name']}(self):
        # TODO: Implement test for {func['name']}
        pass
"""
            test_content += "\nif __name__ == '__main__':\n    unittest.main()"
            (self.output_dir / 'tests' / 'test_functions.py').write_text(
                self.format_code(test_content)
            )

    def _write_main_file(self) -> None:
        """Write the main.py file."""
        main_content = 'from .dependencies import *\n'
        for class_info in self.classes:
            main_content += f'from .{class_info["name"].lower()} import {class_info["name"]}\n'
        if self.functions:
            main_content += 'from .functions import *\n'
        
        main_content += '\n\ndef main():\n    pass\n\n'
        main_content += 'if __name__ == "__main__":\n    main()\n'
        
        (self.output_dir / 'main.py').write_text(self.format_code(main_content))

    def _write_documentation(self) -> None:
        """Generate documentation files."""
        # Generate README
        readme_content = f"# {os.path.basename(self.file_path)} Module\n\n"
        readme_content += "## Overview\n\n"
        readme_content += "## Installation\n\n```\npip install -r requirements.txt\n```\n\n"
        readme_content += "## Components\n\n"
        
        # Add classes documentation
        if self.classes:
            readme_content += "### Classes\n\n"
            for class_info in self.classes:
                readme_content += f"- {class_info['name']}\n"
                if class_info['docstring']:
                    readme_content += f"  - {class_info['docstring']}\n"

        # Add functions documentation
        if self.functions:
            readme_content += "\n### Functions\n\n"
            for func in self.functions:
                readme_content += f"- {func['name']}\n"
                if func['docstring']:
                    readme_content += f"  - {func['docstring']}\n"

        (self.output_dir / 'README.md').write_text(readme_content)

    def _write_setup_file(self) -> None:
        """Write setup.py file."""
        setup_content = f"""from setuptools import setup, find_packages

setup(
    name="{os.path.basename(self.output_dir)}",
    version="0.1.0",
    packages=find_packages(),
    install_requires={list(self.dependencies)},
    author="",
    author_email="",
    description="Generated from {os.path.basename(self.file_path)}",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.13",
)"""
        (self.output_dir / 'setup.py').write_text(self.format_code(setup_content))

def main():
    """Main function to run the code analyzer."""
    try:
        file_path = input("Enter the path to your Python file: ")
        if not os.path.exists(file_path):
            print("File not found!")
            return

        analyzer = CodeAnalyzer(file_path)
        print("Parsing file...")
        analyzer.parse_file()
        
        print("Analyzing code...")
        analyzer.analyze_code()
        
        print("Creating module structure...")
        analyzer.create_module_structure()
        
        print(f"\nCode has been modularized and saved in: {analyzer.output_dir}")
        print("Generated files include:")
        print("- Modular code files")
        print("- Unit tests")
        print("- Documentation")
        print("- Requirements file")
        print("- Setup file")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()