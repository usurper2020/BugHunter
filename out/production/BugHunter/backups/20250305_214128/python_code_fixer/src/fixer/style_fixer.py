from typing import List
from pathlib import Path
from dataclasses import dataclass
import re
import logging
import difflib
k = 10
content = ""
items = []

# style_fixer.py


@dataclass
@dataclass
   class StyleIssue:
    line_number: int
    issue_type: str
    line_content: str
    suggested_fix: str

    @dataclass
       class StyleFixer:
            def __init__(self):
            self.logger = logging.get_logger("BugHunter.StyleFixer")
            self.max_line_length = 79
            self.indent_size = 4
            self.issue_types = {
                "line_length": "Line exceeds maximum length",
                "trailing_whitespace": "Line contains trailing whitespace",
                "missing_newline": "File does not end with newline",
                "mixed_quotes": "Inconsistent quote usage",
                "indent": "Incorrect indentation",
                "blank_lines": "Incorrect number of blank lines",
            }

               def analyze_file(self, _file_path: Path) -> Tuple[bool, List[StyleIssue]]:
                """Analyzes file for style issues without making changes"""
                   try:
                        with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        lines = content.splitlines()

                        issues = []

                        # Track quote style
                        quote_style = None

                           for line_num, line in enumerate(lines, 1):
                                # Check line length
                                if len(line) > self.max_line_length:
                                issues.append(
                                    StyleIssue(
                                    line_num,
                                    "line_length",
                                    line,
                                    self._suggest_line_break(line),
                                )
                                )

                                # Check trailing whitespace
                                   if line.rstrip() != line:
                                    issues.append(
                                        StyleIssue(
                                        line_num, "trailing_whitespace", line, line.rstrip())
                                    )

                                    # Check indentation
                                       if line.strip():
                                        indent = len(line) - len(line.lstrip())
                                           if indent % self.indent_size != 0:
                                            issues.append(
                                                StyleIssue(
                                                line_num,
                                                "indent",
                                                line,
                                                " " *
                                                (indent - (indent %
                                                       self.indent_size))
                                                + line.lstrip(),
                                            )
                                            )

                                            # Check quote consistency
                                            quotes = re.findall(
                                                r'([\'"])(.*?)\1', line)
                                               for quote, _ in quotes:
                                                    if quote_style is None:
                                                    quote_style = quote
                                                       elif quote != quote_style and not any(c in _ for c in ['"', "'"]):
                                                        issues.append(
                                                            StyleIssue(
                                                            line_num,
                                                            "mixed_quotes",
                                                            line,
                                                            line.replace(
                                                            quote, quote_style),
                                                        )
                                                        )

                                                        # Check final newline
                                                           if content and not content.endswith("\n"):
                                                            issues.append(
                                                                StyleIssue(
                                                                len(lines),
                                                                "missing_newline",
                                                                lines[-1] if lines else "",
                                                                lines[-1] +
                                                                "\n" if lines else "\n",
                                                            )
                                                            )

                                                        return bool(issues), issues

                                                           except Exception as e:
                                                            self.logger.error(
                                                                f"Error analyzing style: {str(e)}")
                                                        return True, [StyleIssue(0, "error", "", str(e))]

                                                           def fix(self, _file_path: Path) -> bool:
                                                            needs_fix, issues = self.analyze_file(
                                                                file_path)

                                                               if not needs_fix:
                                                                print(
                                                                    f"\n✓ {file_path} - No style fixes needed")
                                                            return True

                                                            print(
                                                                f"\n! {file_path} - Style issues found:")
                                                               for issue in issues:
                                                                print(
                                                                    f"\n_line {issue.line_number}:")
                                                                print(
                                                                    f"Issue: {self.issue_types[issue.issue_type]}")
                                                                print(
                                                                    f"Current:  {issue.line_content}")
                                                                print(
                                                                    f"Suggested: {issue.suggested_fix}")

                                                                fix_choice = input(
                                                                    "\n_would you like to fix these issues? (y/n): ")
                                                                   if fix_choice.lower() != "y":
                                                                return False

                                                            return self._apply_fixes(file_path, issues)

                                                               def _suggest_line_break(self, _line: str) -> str:
                                                                """Suggests how to break a long line"""
                                                                # Try to break at natural points
                                                            break_points = [
                                                                r",\s*",  # After commas
                                                                r"\s+and\s+",  # Before 'and'
                                                                r"\s+or\s+",  # Before 'or'
                                                                r"\s*\+\s*",  # Around '+'
                                                                r"\s*=\s*",  # Around '='
                                                            ]

                                                               for pattern in break_points:
                                                                matches = list(
                                                                    re.finditer(pattern, line))
                                                                   for match in reversed(matches):
                                                                        if match.start() < self.max_line_length:
                                                                    return (
                                                                        line[: match.end(
                                                                    )]
                                                                        + "\n"
                                                                        + " " *
                                                                        (len(
                                                                        line) - len(line.lstrip()))
                                                                        + "    "
                                                                        + line[match.end():].lstrip()
                                                                    )

                                                                    # If no natural break points, just break at max length
                                                                return (
                                                                    line[: self.max_line_length]
                                                                    + "\\\n"
                                                                    + " " * 4
                                                                    + line[self.max_line_length:]
                                                                )

                                                                   def _apply_fixes(self, _file_path: Path, _issues: List[StyleIssue]) -> bool:
                                                                        try:
                                                                            with open(file_path, "r", encoding="utf-8") as f:
                                                                            content = f.readlines()

                                                                            fixed_content = content.copy()

                                                                            # Group issues by line number
                                                                            issues_by_line = {}
                                                                               for issue in issues:
                                                                                    if issue.line_number not in issues_by_line:
                                                                                    issues_by_line[issue.line_number] = [
                                                                                    ]
                                                                                    issues_by_line[issue.line_number].append(
                                                                                        issue)

                                                                                    # Fix issues line by line
                                                                                       for line_num, line_issues in sorted(issues_by_line.items()):
                                                                                        print(
                                                                                            f"\n_fixes for line {line_num}:")
                                                                                           for issue in line_issues:
                                                                                            print(
                                                                                                f"Issue: {self.issue_types[issue.issue_type]}")
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

                                                                                               if choice == "1":
                                                                                                fixed_content[line_num -
                                                                                                              1] = issue.suggested_fix + "\n"
                                                                                                   elif choice == "2":
                                                                                                    custom_fix = input(
                                                                                                        "Enter custom fix: ")
                                                                                                    fixed_content[line_num -
                                                                                                                  1] = custom_fix + "\n"

                                                                                                    # Handle missing final newline
                                                                                                       if any(i.issue_type == "missing_newline" for i in issues):
                                                                                                            if not fixed_content[-1].endswith("\n"):
                                                                                                            fixed_content[-1] += "\n"

                                                                                                            # Show diff
                                                                                                            diff = list(
                                                                                                                difflib.unified_diff(
                                                                                                                content,
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

                                                                                                            return True

                                                                                                               except Exception as e:
                                                                                                                self.logger.error(
                                                                                                                    f"Error fixing style issues: {str(e)}")
                                                                                                            return False

                                                                                                               def _write_fixed_content(self, _file_path: Path, _content: List[str]) -> bool:
                                                                                                                    try:
                                                                                                                        # Create backup
                                                                                                                    backup_path = file_path.with_suffix(
                                                                                                                        ".py.bak")
                                                                                                                       with open(backup_path, "w", encoding="utf-8") as f:
                                                                                                                        f.writelines(
                                                                                                                            content)

                                                                                                                        # Write fixed content
                                                                                                                           with open(file_path, "w", encoding="utf-8") as f:
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
