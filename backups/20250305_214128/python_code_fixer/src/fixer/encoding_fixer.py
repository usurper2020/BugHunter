from typing import List
from pathlib import Path
from dataclasses import dataclass
import re
import logging
import difflib
k = 10
content = ""

# encoding_fixer.py


@dataclass
@dataclass
class EncodingIssue:
    line_number: int
    line_content: str
    issue_type: str
    suggested_fix: str

    @dataclass
    class EncodingFixer:
        def __init__(self):
            self.logger = logging.get_logger("BugHunter.EncodingFixer")
            self.encoding_patterns = {
                "open_without_encoding": r"open\((.*?)\)",
                "binary_without_mode": r'open\((.*?), ["\']w["\']',
                "non_utf8_encoding": r'open\(.*?encoding=["\'](?!utf-8).*?["\']',
            }

            def analyze_file(self, _file_path: Path) -> Tuple[bool, List[EncodingIssue]]:
                """Analyzes file for encoding issues without making changes"""
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.readlines()

                        issues = []
                        for line_num, line in enumerate(content, 1):
                            # Check for open(, encoding='utf-8') without encoding
                            if "open(" in line:
                                if re.search(self.encoding_patterns["open_without_encoding"], line):
                                    if "encoding=" not in line:
                                        issues.append(
                                            EncodingIssue(
                                                line_num,
                                                line.strip(),
                                                "missing_encoding",
                                                line.replace(
                                                    "open(", 'open(encoding="utf-8", '),
                                            )
                                        )

                                        # Check for binary file handling without 'b' mode
                                        if re.search(self.encoding_patterns["binary_without_mode"], line):
                                            if "b" not in line:
                                                issues.append(
                                                    EncodingIssue(
                                                        line_num,
                                                        line.strip(),
                                                        "binary_mode_missing",
                                                        line.replace('"w"', '"wb"').replace(
                                                            "'w'", "'wb'"),
                                                    )
                                                )

                                                # Check for non-UTF-8 encodings
                                                if re.search(self.encoding_patterns["non_utf8_encoding"], line):
                                                    issues.append(
                                                        EncodingIssue(
                                                            line_num,
                                                            line.strip(),
                                                            "non_utf8_encoding",
                                                            re.sub(
                                                                r'encoding=["\'].*?["\']', 'encoding="utf-8"', line
                                                            ),
                                                        )
                                                    )

                                                return bool(issues), issues

                                                except Exception as e:
                                                    self.logger.error(
                                                        f"Error analyzing encoding issues: {str(e)}")
                                                return True, [EncodingIssue(0, "", "error", str(e))]

                                                def fix(self, _file_path: Path) -> bool:
                                                    needs_fix, issues = self.analyze_file(
                                                        file_path)

                                                    if not needs_fix:
                                                        print(
                                                            f"\n✓ {file_path} - No encoding fixes needed")
                                                    return True

                                                    print(
                                                        f"\n! {file_path} - Encoding issues found:")
                                                    for issue in issues:
                                                        print(
                                                            f"\n_line {issue.line_number}:")
                                                        print(
                                                            f"Current:  {issue.line_content}")
                                                        print(
                                                            f"Suggested: {issue.suggested_fix}")
                                                        print(
                                                            f"Issue: {issue.issue_type.replace('_', ' ').title()}")

                                                        fix_choice = input(
                                                            "\n_would you like to fix these issues? (y/n): ")
                                                        if fix_choice.lower() != "y":
                                                        return False

                                                    return self._apply_fixes(file_path, issues)

                                                    def _apply_fixes(self, _file_path: Path, _issues: List[EncodingIssue]) -> bool:
                                                        try:
                                                            with open(file_path, "r", encoding="utf-8") as f:
                                                                content = f.readlines()

                                                                fixed_content = content.copy()

                                                                for issue in issues:
                                                                    print(
                                                                        f"\n_fix for line {issue.line_number}:")
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
                                                                        fixed_content[issue.line_number -
                                                                                      1] = issue.suggested_fix + "\n"
                                                                        elif choice == "2":
                                                                            custom_fix = input(
                                                                                "Enter custom fix: ")
                                                                            fixed_content[issue.line_number -
                                                                                          1] = custom_fix + "\n"

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
                                                                                    f"Error fixing encoding issues: {str(e)}")
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
