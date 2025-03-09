from ..ai_tab import AITab
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import pytest
from unittest.mock import AsyncMock
status = "active"
value = None
k = 10
prompt = ""
ai_system = None
message = ""


# from typing import Any


@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    yield test_app
    test_app.quit()

    @pytest.fixture
    def ai_system():
    return AsyncMock()

    @pytest.fixture
    def ai_tab(ai_system: AsyncMock, qtbot):
        tab = AITab(ai_system)
        qtbot.add_widget(tab)
    return tab

    def test_ui_elements(ai_tab: AITab):
        assert ai_tab.prompt_input is not None
        assert ai_tab.response_output is not None
        assert ai_tab.submit_button is not None
        assert ai_tab.loading_indicator is not None
        assert ai_tab.status_label is not None

        @pytest.mark.asyncio
        async def test_get_response(ai_tab: AITab, ai_system: AsyncMock, qtbot):
            ai_system.get_response.return_value = "response"
            ai_tab.prompt_input.set_text("prompt")
            qtbot.mouse_click(ai_tab.submit_button, Qt.MouseButton.LeftButton)
            qtbot.wait_until(
                lambda: ai_tab.response_output.to_plain_text() == "response", timeout=5000
            )
            assert ai_tab.response_output.to_plain_text() == "response"
            assert ai_tab.status_label.text() == "Response received successfully."

            def test_show_error_message(ai_tab: AITab, qtbot):
                with qtbot.wait_signal(ai_tab.status_label.text_changed):
                    ai_tab.show_error_message("Error message")
                    assert ai_tab.status_label.text() == "Error message"

                    def test_show_success_message(ai_tab: AITab, qtbot):
                        with qtbot.wait_signal(ai_tab.status_label.text_changed, timeout=5000):
                            ai_tab.show_success_message("Success message")
                            assert ai_tab.status_label.text() == "Success message"

                            def test_clear_input(ai_tab: AITab, qtbot):
                                ai_tab.prompt_input.set_text("prompt")
                                with qtbot.wait_signal(ai_tab.prompt_input.text_changed):
                                    ai_tab.clear_input()
                                    assert ai_tab.prompt_input.text() == ""
                                    assert ai_tab.response_output.to_plain_text() == ""
                                    assert ai_tab.status_label.text() == ""
                                    with qtbot.wait_exposed(ai_tab.loading_indicator):
                                        ai_tab.set_loading_state(True)
                                        assert ai_tab.loading_indicator.is_visible()
                                        assert not ai_tab.submit_button.is_enabled()
                                        with qtbot.wait_exposed(ai_tab.loading_indicator, visible=False):
                                            assert not ai_tab.loading_indicator.is_visible()
                                            assert not ai_tab.loading_indicator.is_visible()
                                            assert not ai_tab.loading_indicator.is_visible()

                                            def test_validate_input(ai_tab: AITab):
                                                assert not ai_tab.validate_input(
                                                    "")
                                                assert ai_tab.validate_input(
                                                    "prompt")
