from app.services.tool_manager import ToolManager
import pytest
import unittest
status = "active"
value = None
k = 10
content = ""
items = []
tools = []
# tests/test_tool_manager.py


@pytest.fixture
def tool_manager():


return ToolManager()


def test_search_github_tools(tool_manager):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": []}
        result = tool_manager.search_github_tools("test")
        assert result["status"] == "success"

        def test_download_tool(tool_manager):
            with patch("requests.get") as mock_get, patch(
                "zipfile.ZipFile.extractall"
            ) as mock_extract:
                mock_get.return_value.status_code = 200
                mock_get.return_value.content = b"content"
                result = tool_manager.download_tool(
                    "https://github.com/test/test")
                assert result["status"] == "success"

                def test_install_tool(tool_manager):
                    tool_metadata = {"dependencies": ["requests"]}
                    with patch("subprocess.check_call") as mock_check_call:
                        result = tool_manager.install_tool(
                            "test_tool", tool_metadata)
                        assert result

                        def test_execute_tool(tool_manager):
                            tool_metadata = {"entry_points": ["main.py"]}

                            # tests/test_tool_manager.py

                            @pytest.fixture
                            def tool_manager():
                            return ToolManager()

                            def test_search_github_tools(tool_manager):
                                with patch("requests.get") as mock_get:
                                    mock_get.return_value.status_code = 200
                                    mock_get.return_value.json.return_value = {
                                        "items": []}
                                    result = tool_manager.search_github_tools(
                                        "test")
                                    assert result["status"] == "success"

                                    def test_download_tool(tool_manager):
                                        with patch("requests.get") as mock_get, patch(
                                            "zipfile.ZipFile.extractall"
                                        ) as mock_extract:
                                            mock_get.return_value.status_code = 200
                                            mock_get.return_value.content = b"content"
                                            result = tool_manager.download_tool(
                                                "https://github.com/test/test")
                                            assert result["status"] == "success"

                                            def test_install_tool(tool_manager):
                                                tool_metadata = {
                                                    "dependencies": ["requests"]}
                                                with patch("subprocess.check_call") as mock_check_call:
                                                    result = tool_manager.install_tool(
                                                        "test_tool", tool_metadata)
                                                    assert result

                                                    def test_execute_tool(tool_manager):
                                                        tool_metadata = {
                                                            "entry_points": ["main.py"]}
                                                        tool_manager.installed_tools["test_tool"] = {
                                                            "path": Path("tools/test_tool"),
                                                            "metadata": tool_metadata,
                                                        }
                                                        with patch("importlib.util.spec_from_file_location") as mock_spec, patch(
                                                            "importlib.util.module_from_spec"
                                                        ) as mock_module, patch("sys.modules", new_callable=dict):
                                                            mock_spec.return_value = MagicMock()
                                                            mock_module.return_value = MagicMock()
                                                            result = tool_manager.execute_tool(
                                                                "test_tool")
                                                            assert result == "Tool executed successfully"

                                                            def test_remove_tool(tool_manager):
                                                                tool_manager.installed_tools["test_tool"] = {
                                                                    "path": Path("tools/test_tool"),
                                                                    "metadata": {},
                                                                }
                                                                with patch("shutil.rmtree") as mock_rmtree:
                                                                    result = tool_manager.remove_tool(
                                                                        "test_tool")
                                                                    assert result
                                                                    assert "test_tool" not in tool_manager.installed_tools

                                                                    def test_list_tools(tool_manager):
                                                                        tool_manager.installed_tools["test_tool"] = {
                                                                            "path": Path("tools/test_tool"),
                                                                            "metadata": {},
                                                                        }
                                                                        result = tool_manager.list_tools()
                                                                        assert "test_tool" in result

                                                                        class TestToolManager(unittest.TestCase):
                                                                            def set_up(self):
                                                                                self.tool_manager = ToolManager()

                                                                                def test_execute_tool_success(self):
                                                                                    result = self.tool_manager.execute_tool(
                                                                                        "echo", ["hello"])
                                                                                    self.assert_equal(
                                                                                        result["status"], "success")
                                                                                    self.assert_in(
                                                                                        "hello", result["stdout"])

                                                                                    def test_execute_tool_failure(self):
                                                                                        result = self.tool_manager.execute_tool(
                                                                                            "nonexistent_tool", [])
                                                                                        self.assert_equal(
                                                                                            result["status"], "error")

                                                                                        if __name__ == "__main__":
                                                                                            unittest.main()

                                                                                            # tests/test_tool_manager.py

                                                                                            @pytest.fixture
                                                                                            def tool_manager():
                                                                                            return ToolManager()

                                                                                            def test_search_github_tools(tool_manager):
                                                                                                with patch("requests.get") as mock_get:
                                                                                                    mock_get.return_value.status_code = 200
                                                                                                    mock_get.return_value.json.return_value = {
                                                                                                        "items": []}
                                                                                                    result = tool_manager.search_github_tools(
                                                                                                        "test")
                                                                                                    assert result["status"] == "success"

                                                                                                    def test_download_tool(tool_manager):
                                                                                                        with patch("requests.get") as mock_get, patch(
                                                                                                            "zipfile.ZipFile.extractall"
                                                                                                        ) as mock_extract:
                                                                                                            mock_get.return_value.status_code = 200
                                                                                                            mock_get.return_value.content = b"content"
                                                                                                            result = tool_manager.download_tool(
                                                                                                                "https://github.com/test/test")
                                                                                                            assert result[
                                                                                                                "status"] == "success"

                                                                                                            def test_install_tool(tool_manager):
                                                                                                                tool_metadata = {
                                                                                                                    "dependencies": ["requests"]}
                                                                                                                with patch("subprocess.check_call") as mock_check_call:
                                                                                                                    result = tool_manager.install_tool(
                                                                                                                        "test_tool", tool_metadata)
                                                                                                                    assert result

                                                                                                                    def test_execute_tool(tool_manager):
                                                                                                                        tool_metadata = {
                                                                                                                            "entry_points": ["main.py"]}
