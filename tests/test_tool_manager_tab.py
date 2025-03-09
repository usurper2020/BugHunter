from app.services.tool_manager import ToolManager
from app.gui.tabs.tool_manager_tab import ToolManagerTab
from PyQt6.QtWidgets import QApplication
import pytest
status = "active"
value = None
url = ""
k = 10
tools = []
# tests/test_tool_manager_tab.py


@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    yield test_app
    test_app.quit()

    @pytest.fixture
    def tool_manager():
    return MagicMock(spec=ToolManager)

    @pytest.fixture
    def tool_manager_tab(tool_manager, qtbot):
        tab = ToolManagerTab(tool_manager)
        qtbot.add_widget(tab)
    return tab

    def test_ui_elements(tool_manager_tab):
        assert tool_manager_tab.search_input is not None
        assert tool_manager_tab.search_button is not None
        assert tool_manager_tab.results_table is not None
        assert tool_manager_tab.progress_bar is not None
        assert tool_manager_tab.status_bar is not None
        assert tool_manager_tab.installed_table is not None

        def test_search_tools(tool_manager_tab, tool_manager, qtbot):
            tool_manager.search_github_tools.return_value = {
                "status": "success", "results": []}
            tool_manager_tab.search_input.set_text("test")
            qtbot.mouse_click(tool_manager_tab.search_button, qtbot.LeftButton)
            tool_manager.search_github_tools.assert_called_once_with("test")

            def test_install_tool(tool_manager_tab, tool_manager, qtbot):
                tool_manager.download_tool.return_value = {
                    "status": "success",
                    "tool_name": "test_tool",
                }
                tool_manager_tab.install_tool(
                    {"html_url": "https://github.com/test/test"})
                tool_manager.download_tool.assert_called_once_with(
                    "https://github.com/test/test")

                def test_remove_tool(tool_manager_tab, tool_manager, qtbot):
                    tool_manager.remove_tool.return_value = True
                    tool_manager_tab.remove_tool("test_tool")
                    tool_manager.remove_tool.assert_called_once_with(
                        "test_tool")
