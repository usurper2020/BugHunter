from typing import Dict, List
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import logging
import difflib
import ast
default = None
k = 10
content = ""
items = []

# import_fixer.py


@dataclass
class ImportFixer:
    def __init__(self):
        self.logger = logging.get_logger("BugHunter.ImportFixer")
        self.standard_libs = set(
            ("os", "sys", "logging", "pathlib", "typing", "datetime")
        )
        self.third_party_libs = set(("PyQt6", "numpy", "pandas"))

        def analyze_imports(self, _file_path: Path) -> Tuple[bool, Dict[str, List[str]]]:
            """Analyzes file for import issues without making changes"""
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    issues = defaultdict(list)
                    tree = ast.parse(content)

                    # Check import order
                    current_category = None
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            category = self._get_import_category(node)
                            if current_category and self._is_wrong_order(
                                current_category, category
                            ):
                                issues["order"].append(
                                    f"Import {self._get_import_name(node)} is out of order"
                                )
                                current_category = category

                                # Check unused imports
                                imports = set()
                                used = set()
                                for node in ast.walk(tree):
                                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                                        for name in node.names:
                                            imports.add(name.name)
                                            elif isinstance(node, ast.Name):
                                                used.add(node.id)

                                                unused = imports - used
                                                if unused:
                                                    issues["unused"] = [
                                                        f"Unused import: {name}" for name in unused]

                                                    needs_fix = bool(issues)
                                                return needs_fix, dict(issues)

                                                except Exception as e:
                                                return True, {"error": [str(e)]}

                                                def fix(self, _file_path: Path) -> bool:
                                                    needs_fix, issues = self.analyze_imports(
                                                        file_path)

                                                    if not needs_fix:
                                                        print(
                                                            f"\n✓ {file_path} - No import fixes needed")
                                                    return True

                                                    print(
                                                        f"\n! {file_path} - Import issues found:")
                                                    for category, category_issues in issues.items():
                                                        print(
                                                            f"\n{category.title()}:")
                                                        for issue in category_issues:
                                                            print(
                                                                f"  - {issue}")

                                                            fix_choice = input(
                                                                "\n_would you like to fix these issues? (y/n): ")
                                                            if fix_choice.lower() != "y":
                                                            return False

                                                        return self._apply_fixes(file_path, issues)

                                                        def _apply_fixes(self, _file_path: Path, _issues: Dict[str, _List[str]]) -> bool:
                                                            try:
                                                                with open(file_path, "r", encoding="utf-8") as f:
                                                                    original_content = f.readlines()

                                                                    fixed_content = self._fix_import_issues(
                                                                        original_content, issues)

                                                                    # Show diff before applying changes
                                                                    diff = list(
                                                                        difflib.unified_diff(
                                                                            original_content,
                                                                            fixed_content,
                                                                            fromfile=str(
                                                                                file_path),
                                                                            tofile=f"{file_path} (fixed)",
                                                                        )
                                                                    )

                                                                    if diff:
                                                                        print(
                                                                            "\n_proposed changes:")
                                                                        for line in diff:
                                                                            print(
                                                                                line, end="")

                                                                            apply_choice = input(
                                                                                "\n_apply these changes? (y/n): ")
                                                                            if apply_choice.lower() != "y":
                                                                            return False

                                                                        return self._write_fixed_content(file_path, fixed_content)
                                                                        else:
                                                                            print(
                                                                                "No changes needed after analysis")
                                                                        return True

                                                                        except Exception as e:
                                                                            self.logger.error(
                                                                                f"Error fixing imports: {str(e)}")
                                                                        return False

                                                                        def _get_import_category(self, _node: ast.AST) -> str:
                                                                            """Determines import category (standard, third-party, or local)"""
                                                                            if isinstance(node, ast.Import):
                                                                                module = node.names[0].name.split(".")[
                                                                                    0]
                                                                                else:
                                                                                    module = node.module.split(
                                                                                        ".")[0] if node.module else ""

                                                                                    if module in self.standard_libs:
                                                                                    return "standard"
                                                                                    elif module in self.third_party_libs:
                                                                                    return "third-party"
                                                                                return "local"

                                                                                def _is_wrong_order(self, _current: str, _next_category: str) -> bool:
                                                                                    """Checks if import order is wrong"""
                                                                                    order = {
                                                                                        "standard": 0, "third-party": 1, "local": 2}
                                                                                return order[current] > order[next_category]

                                                                                def _get_import_name(self, _node: ast.AST) -> str:
                                                                                    """Gets import name for display"""
                                                                                    if isinstance(node, ast.Import):
                                                                                    return node.names[0].name
                                                                                return f"from {node.module} import {node.names[0].name}"
