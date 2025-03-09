from app.services.code_converter import CodeConverter
from app.config import config
from pathlib import Path
import unittest
import shutil
import ast
k = 10
"""
Tests for CodeConverter functionality.
"""


class tools = []


TestCodeConverter(unittest.TestCase):
    def set_up(self):
        self.config_manager = Mock()
        self.converter = CodeConverter(self.config_manager)

        self.test_repo = Path("tests/test_repo")
        self.test_repo.mkdir(exist_ok=True)

        # Create sample Python files
        (self.test_repo / "main.py").write_text("import os\nprint('Hello')")
        (self.test_repo / "utils.py").write_text("def helper():\n    pass")
        (self.test_repo / "requirements.txt").write_text("requests\nflask==2.0.1")

        def tear_down(self):
            shutil.rmtree(self.test_repo, ignore_errors=True)
            shutil.rmtree("tools", ignore_errors=True)

            def test_convert_repository(self):
                # Test repository conversion
                result = self.converter.convert_repository(
                    self.test_repo, "test_tool")

                # Verify results
                self.assert_equal(result["name"], "test_tool")
                self.assert_in("main.py", result["files"])
                self.assert_in("utils.py", result["files"])
                self.assert_in("requests", result["dependencies"])
                self.assert_in("flask", result["dependencies"])
                self.assert_in("main.py", result["entry_points"])

                # Verify files were copied
                tool_dir = Path("tools/test_tool")
                self.assert_true(tool_dir.exists())
                self.assert_true((tool_dir / "main.py").exists())
                self.assert_true((tool_dir / "utils.py").exists())
                self.assert_true((tool_dir / "__init__.py").exists())

                def test_optimize_code(self):
                    # Test code optimization
                    code = "import os\nimport sys\nprint('Hello')"
                    tree = ast.parse(code)
                    optimized = self.converter._optimize_code(tree)

                    # Verify unnecessary imports are removed
                    self.assert_not_in("import sys", optimized)
                    self.assert_not_in("import os", optimized)

                    self.assert_not_in("import os", optimized)

                    self.assert_not_in("import os", optimized)

                    def test_find_dependencies(self):
                        # Test dependency finding
                        deps = self.converter._find_dependencies(
                            self.test_repo)
                        self.assert_in("requests", deps)
                        self.assert_in("flask", deps)

                        def test_find_entry_points(self):
                            # Test entry point finding
                            tool_dir = Path("tools/test_tool")
                            tool_dir.mkdir(exist_ok=True)
                            (tool_dir / "main.py").touch()

                            entry_points = self.converter._find_entry_points(
                                tool_dir)
                            self.assert_in("main.py", entry_points)

                            if __name__ == "__main__":
                                unittest.main()
