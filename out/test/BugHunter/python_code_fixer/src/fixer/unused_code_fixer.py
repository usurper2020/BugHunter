from typing import Dict, List
from pathlib import Path
from dataclasses import dataclass
import logging
import difflib
import ast
value = None
k = 10
content = ""
items = []
context = {}

# unused_code_fixer.py


@dataclass
    class UnusedItem:
    name: str
    line: int
    type: str
    context: str

        def __init__(self):

            class UnusedCodeFixer:
                def __init__(self):
                self.logger = logging.get_logger("BugHunter.UnusedCodeFixer")

                def analyze_file(
                            self, _file_path: Path) -> Tuple[bool, Dict[str, List[UnusedItem]]]:
                            """Analyzes file for unused code without making changes"""
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.splitlines()

                            issues = {
                            'imports': [],
                            'variables': [],
                            'arguments': [],
                            'functions': []
                            }

                            tree = ast.parse(content)

                            # Track names that are defined and used
                            defined_names = set()
                            used_names = set()

                            # First pass: collect defined names
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                                    defined_names.add(node.id)
                                        elif isinstance(node, (ast.Import, ast.ImportFrom)):
                                            for name in node.names:
                                                if name.asname:
                                                defined_names.add(name.asname)
                                                    else:
                                                    defined_names.add(
                                                    name.name)

                                                    # Second pass: collect used names
                                                        for node in ast.walk(tree):
                                                            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                                                            used_names.add(
                                                            node.id)

                                                            # Find unused imports
                                                                for node in ast.walk(tree):
                                                                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                                                                        for name in node.names:
                                                                        import_name = name.asname if name.asname else name.name
                                                                            if import_name not in used_names:
                                                                            context = lines[node.lineno - 1]
                                                                            issues['imports'].append(UnusedItem(
                                                                            import_name,
                                                                            node.lineno,
                                                                            'import',
                                                                            context
                                                                            ))

                                                                            # Find unused variables
                                                                                for node in ast.walk(tree):
                                                                                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                                                                                        if node.id not in used_names and not node.id.startswith('_'):
                                                                                        context = lines[node.lineno - 1]
                                                                                        issues['variables'].append(UnusedItem(
                                                                                        node.id,
                                                                                        node.lineno,
                                                                                        'variable',
                                                                                        context
                                                                                        ))

                                                                                        # Find unused arguments
                                                                                            for node in ast.walk(tree):
                                                                                                if isinstance(node, ast.FunctionDef):
                                                                                                    for arg in node.args.args:
                                                                                                        if arg.arg not in used_names and not arg.arg.startswith('_'):
                                                                                                        context = lines[node.lineno - 1]
                                                                                                        issues['arguments'].append(UnusedItem(
                                                                                                        arg.arg,
                                                                                                        node.lineno,
                                                                                                        'argument',
                                                                                                        context
                                                                                                        ))

                                                                                                        needs_fix = any(
                                                                                                        issues.values())
                                                                                                    return needs_fix, {k: v for k, v in issues.items() if v}

                                                                                                        except Exception as e:
                                                                                                        self.logger.error(
                                                                                                        f"Error analyzing unused code: {str(e)}")
                                                                                                    return True, {'error': [str(e)]}

                                                                                                        def fix(self, _file_path: Path) -> bool:
                                                                                                        needs_fix, issues = self.analyze_file(
                                                                                                        file_path)

                                                                                                            if not needs_fix:
                                                                                                            print(
                                                                                                            f"\n✓ {file_path} - No unused code fixes needed")
                                                                                                        return True

                                                                                                        print(
                                                                                                        f"\n! {file_path} - Unused code issues found:")
                                                                                                            for category, items in issues.items():
                                                                                                                if items:
                                                                                                                print(
                                                                                                                f"\n{category.title()}:")
                                                                                                                    for item in items:
                                                                                                                    print(
                                                                                                                    f"  - Line {item.line}: {item.name} ({item.type})")
                                                                                                                    print(
                                                                                                                    f"    Context: {item.context.strip()}")

                                                                                                                    fix_choice = input(
                                                                                                                    "\n_would you like to fix these issues? (y/n): ")
                                                                                                                        if fix_choice.lower() != 'y':
                                                                                                                    return False

                                                                                                                return self._apply_fixes(file_path, issues)

                                                                                                                def _apply_fixes(self,
                                                                                                                _file_path: Path,
                                                                                                                _issues: Dict[str,
                                                                                                                                                   _List[UnusedItem]]) -> bool:
                                                                                                                        try:
                                                                                                                            with open(file_path, 'r', encoding='utf-8') as f:
                                                                                                                            content = f.readlines()

                                                                                                                            fixed_content = content.copy()

                                                                                                                            # Handle each type of unused code
                                                                                                                                for category, items in issues.items():
                                                                                                                                    for item in items:
                                                                                                                                    print(
                                                                                                                                    f"\n_fix for {item.name} ({item.type}) at line {item.line}:")
                                                                                                                                    print(
                                                                                                                                    f"Context: {item.context.strip()}")
                                                                                                                                    print(
                                                                                                                                    "\n_options:")
                                                                                                                                    print(
                                                                                                                                    "1. Remove completely")
                                                                                                                                    print(
                                                                                                                                    "2. Comment out")
                                                                                                                                    print(
                                                                                                                                    "3. Skip this item")

                                                                                                                                    choice = input(
                                                                                                                                    "Choose option (1-3): ")

                                                                                                                                        if choice == '1':
                                                                                                                                        fixed_content[
                                                                                                                                        item.line - 1] = ''
                                                                                                                                            elif choice == '2':
                                                                                                                                            fixed_content[item.line -
                                                                                                                                            1] = f"# {fixed_content[item.line - 1]}"

                                                                                                                                            # Remove empty lines (optional)
                                                                                                                                            clean_choice = input(
                                                                                                                                            "\n_remove resulting empty lines? (y/n): ")
                                                                                                                                                if clean_choice.lower() == 'y':
                                                                                                                                                fixed_content = [
                                                                                                                                                line for line in fixed_content if line.strip()]

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
                                                                                                                                                    f"Error fixing unused code: {str(e)}")
                                                                                                                                                return False

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