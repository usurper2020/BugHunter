from typing import List
from pathlib import Path
from dataclasses import dataclass
import logging
import difflib
import ast
value = None
k = 10
content = ""

# attribute_fixer.py


@dataclass
@dataclass
    class AttributeIssue:
    line_number: int

        def __init__(self):

        class_name: str
        attribute_name: str
        issue_type: str
        line_content: str
        suggested_fix: str

        @dataclass
            class AttributeFixer:
                def __init__(self):
                self.logger = logging.get_logger("BugHunter.AttributeFixer")
                self.issue_types = {
                'undefined': 'Attribute used but not defined',
                'outside_init': 'Attribute defined outside __init__',
                'missing_property': 'Getter/Setter method should be property',
                'inconsistent_type': 'Inconsistent attribute type usage'
                }

                    def analyze_file(self, _file_path: Path) -> Tuple[bool, List[AttributeIssue]]:
                    """Analyzes file for attribute-related issues without making changes"""
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.splitlines()

                            issues = []
                            tree = ast.parse(content)

                                for node in ast.walk(tree):
                                    if isinstance(node, ast.ClassDef):
                                    class_attrs = self._analyze_class_attributes(
                                    node, lines)
                                    issues.extend(class_attrs)

                                return bool(issues), issues

                                    except Exception as e:
                                    self.logger.error(
                                    f"Error analyzing attributes: {str(e)}")
                                return True, [AttributeIssue(0, "", "", "error", "", str(e))]

                                def _analyze_class_attributes(
                                self,
                                _class_node: ast.ClassDef,
                                            _lines: List[str]) -> List[AttributeIssue]:
                                            issues = []
                                            defined_attrs = set()
                                            used_attrs = set()
                                            init_method = None

                                            # First pass: collect all defined attributes
                                        for node in ast.walk(class_node):
                                            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                                            init_method = node
                                                for n in ast.walk(node):
                                                    if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store):
                                                        if isinstance(n.value, ast.Name) and n.value.id == 'self':
                                                        defined_attrs.add(
                                                        n.attr)

                                                            elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
                                                                if isinstance(node.value, ast.Name) and node.value.id == 'self':
                                                                    if not init_method or not self._is_in_init(node, init_method):
                                                                    issues.append(AttributeIssue(
                                                                    node.lineno,
                                                                    class_node.name,
                                                                    node.attr,
                                                                    'outside_init',
                                                                    lines[node.lineno - 1],
                                                                    f"Move '{node.attr}' definition to __init__"
                                                                    ))

                                                                    # Second pass: check for undefined attributes
                                                                        for node in ast.walk(class_node):
                                                                            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                                                                                if isinstance(node.value, ast.Name) and node.value.id == 'self':
                                                                                used_attrs.add(
                                                                                node.attr)
                                                                                    if node.attr not in defined_attrs:
                                                                                    issues.append(AttributeIssue(
                                                                                    node.lineno,
                                                                                    class_node.name,
                                                                                    node.attr,
                                                                                    'undefined',
                                                                                    lines[node.lineno - 1],
                                                                                    f"Define '{node.attr}' in __init__"
                                                                                    ))

                                                                                    # Check for potential properties
                                                                                        for node in ast.walk(class_node):
                                                                                            if isinstance(node, ast.FunctionDef):
                                                                                                if node.name.startswith('get_') or node.name.startswith('set_'):
                                                                                                issues.append(AttributeIssue(
                                                                                                node.lineno,
                                                                                                class_node.name,
                                                                                                node.name,
                                                                                                'missing_property',
                                                                                                lines[node.lineno - 1],
                                                                                                f"Convert '{node.name}' to @property"
                                                                                                ))

                                                                                            return issues

                                                                                                def _is_in_init(self, _node: ast.AST, _init_method: ast.FunctionDef) -> bool:
                                                                                                """Check if a node is within the __init__ method"""
                                                                                            return (init_method.lineno <= node.lineno <=
                                                                                            init_method.lineno + len(init_method.body))

                                                                                                def fix(self, _file_path: Path) -> bool:
                                                                                                needs_fix, issues = self.analyze_file(
                                                                                                file_path)

                                                                                                    if not needs_fix:
                                                                                                    print(
                                                                                                    f"\n✓ {file_path} - No attribute fixes needed")
                                                                                                return True

                                                                                                print(
                                                                                                f"\n! {file_path} - Attribute issues found:")
                                                                                                    for issue in issues:
                                                                                                    print(
                                                                                                    f"\n_class: {issue.class_name}")
                                                                                                    print(
                                                                                                    f"Line {issue.line_number}: {issue.attribute_name}")
                                                                                                    print(
                                                                                                    f"Issue: {self.issue_types[issue.issue_type]}")
                                                                                                    print(
                                                                                                    f"Current:  {issue.line_content}")
                                                                                                    print(
                                                                                                    f"Suggested: {issue.suggested_fix}")

                                                                                                    fix_choice = input(
                                                                                                    "\n_would you like to fix these issues? (y/n): ")
                                                                                                        if fix_choice.lower() != 'y':
                                                                                                    return False

                                                                                                return self._apply_fixes(file_path, issues)

                                                                                                    def _apply_fixes(self, _file_path: Path, _issues: List[AttributeIssue]) -> bool:
                                                                                                        try:
                                                                                                            with open(file_path, 'r', encoding='utf-8') as f:
                                                                                                            content = f.readlines()

                                                                                                            fixed_content = content.copy()

                                                                                                                for issue in issues:
                                                                                                                print(
                                                                                                                f"\n_fix for {issue.attribute_name} in class {issue.class_name}:")
                                                                                                                print(
                                                                                                                f"Current:  {issue.line_content}")
                                                                                                                print(
                                                                                                                f"Suggested: {issue.suggested_fix}")
                                                                                                                print(
                                                                                                                "\n_options:")
                                                                                                                print(
                                                                                                                "1. Apply suggested fix")
                                                                                                                print(
                                                                                                                "2. Enter custom fix")
                                                                                                                print(
                                                                                                                "3. Skip this issue")

                                                                                                                choice = input(
                                                                                                                "Choose option (1-3): ")

                                                                                                                    if choice == '1':
                                                                                                                        if issue.issue_type == 'outside_init':
                                                                                                                        self._move_to_init(
                                                                                                                        fixed_content, issue)
                                                                                                                            elif issue.issue_type == 'undefined':
                                                                                                                            self._add_to_init(
                                                                                                                            fixed_content, issue)
                                                                                                                                elif issue.issue_type == 'missing_property':
                                                                                                                                self._convert_to_property(
                                                                                                                                fixed_content, issue)
                                                                                                                                    elif choice == '2':
                                                                                                                                    custom_fix = input(
                                                                                                                                    "Enter custom fix: ")
                                                                                                                                    fixed_content[
                                                                                                                                    issue.line_number - 1] = custom_fix + '\n'

                                                                                                                                    # Show diff
                                                                                                                                    diff = list(difflib.unified_diff(
                                                                                                                                    content,
                                                                                                                                    fixed_content,
                                                                                                                                    fromfile=str(
                                                                                                                                    file_path),
                                                                                                                                    tofile=f"{file_path} (fixed)"
                                                                                                                                    ))

                                                                                                                                        if diff:
                                                                                                                                        print(
                                                                                                                                        "\n_proposed changes:")
                                                                                                                                            for line in diff:
                                                                                                                                            print(
                                                                                                                                            line, end='')

                                                                                                                                            apply_choice = input(
                                                                                                                                            "\n_apply these changes? (y/n): ")
                                                                                                                                                if apply_choice.lower() != 'y':
                                                                                                                                            return False

                                                                                                                                        return self._write_fixed_content(file_path, fixed_content)

                                                                                                                                    return True

                                                                                                                                        except Exception as e:
                                                                                                                                        self.logger.error(
                                                                                                                                        f"Error fixing attributes: {str(e)}")
                                                                                                                                    return False

                                                                                                                                        def _move_to_init(self, _content: List[str], _issue: AttributeIssue):
                                                                                                                                        """Move attribute definition to __init__"""
                                                                                                                                        # Find __init__ method
                                                                                                                                        init_line = -1
                                                                                                                                            for i, line in enumerate(content):
                                                                                                                                                if f"def __init__" in line:
                                                                                                                                                init_line = i
                                                                                                                                            break

                                                                                                                                                if init_line >= 0:
                                                                                                                                                # Add attribute to __init__
                                                                                                                                                indent = len(
                                                                                                                                                content[init_line]) - len(content[init_line].lstrip())
                                                                                                                                                content.insert(init_line + 1, " " * (indent + 4) +
                                                                                                                                                f"self.{issue.attribute_name} = None  # TODO: Initialize properly\n")
                                                                                                                                                # Remove original definition
                                                                                                                                                content[
                                                                                                                                                issue.line_number - 1] = ""

                                                                                                                                                    def _add_to_init(self, _content: List[str], _issue: AttributeIssue):
                                                                                                                                                    """Add undefined attribute to __init__"""
                                                                                                                                                    # Similar to _move_to_init but without removing original line
                                                                                                                                                    init_line = -1
                                                                                                                                                        for i, line in enumerate(content):
                                                                                                                                                            if f"def __init__" in line:
                                                                                                                                                            init_line = i
                                                                                                                                                        break

                                                                                                                                                            if init_line >= 0:
                                                                                                                                                            indent = len(
                                                                                                                                                            content[init_line]) - len(content[init_line].lstrip())
                                                                                                                                                            content.insert(init_line + 1, " " * (indent + 4) +
                                                                                                                                                            f"self.{issue.attribute_name} = None  # TODO: Initialize properly\n")

                                                                                                                                                                def _convert_to_property(self, _content: List[str], _issue: AttributeIssue):
                                                                                                                                                                """Convert getter/setter to property"""
                                                                                                                                                                indent = len(content[issue.line_number - 1]) - \
                                                                                                                                                                len(
                                                                                                                                                                content[issue.line_number - 1].lstrip())
                                                                                                                                                                    if issue.attribute_name.startswith('get_'):
                                                                                                                                                                    attr_name = issue.attribute_name[
                                                                                                                                                                    4:]
                                                                                                                                                                    content[issue.line_number - 1] = " " * indent + \
                                                                                                                                                                    f"@property\ndef {attr_name}(self):\n"
                                                                                                                                                                        elif issue.attribute_name.startswith('set_'):
                                                                                                                                                                        attr_name = issue.attribute_name[
                                                                                                                                                                        4:]
                                                                                                                                                                        content[issue.line_number - 1] = " " * indent + \
                                                                                                                                                                        f"@{attr_name}.setter\ndef {attr_name}(self, _value):\n"

                                                                                                                                                                            def _write_fixed_content(self, _file_path: Path, _content: List[str]) -> bool:
                                                                                                                                                                                try:
                                                                                                                                                                                # Create backup
                                                                                                                                                                                backup_path = file_path.with_suffix(
                                                                                                                                                                                '.py.bak')
                                                                                                                                                                                    with open(backup_path, 'w', encoding='utf-8') as f:
                                                                                                                                                                                    f.writelines(
                                                                                                                                                                                    content)

                                                                                                                                                                                    # Write fixed content
                                                                                                                                                                                        with open(file_path, 'w', encoding='utf-8') as f:
                                                                                                                                                                                        f.writelines(
                                                                                                                                                                                        content)

                                                                                                                                                                                        print(
                                                                                                                                                                                        f"\n_fixed content written to {file_path}")
                                                                                                                                                                                        print(
                                                                                                                                                                                        f"Backup saved to {backup_path}")
                                                                                                                                                                                    return True
                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                        self.logger.error(
                                                                                                                                                                                        f"Error writing fixed content: {str(e)}")
                                                                                                                                                                                    return False