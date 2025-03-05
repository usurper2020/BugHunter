from PyQt6.QtWidgets import QApplication
from unittest.mock import AsyncMock
import pytest
from PyQt6.QtCore import Qt
from unittest.mock import AsyncMock
from ..ai_tab import AITab
# from typing import Any
from PyQt6.QtCore import Qt
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
    qtbot.addWidget(tab)
    return tab

def test_ui_elements(ai_tab: AITab):
    assert ai_tab.prompt_input is not None
    assert ai_tab.response_output is not None
    assert ai_tab.submit_button is not None
    assert ai_tab.loading_indicator is not None
    assert ai_tab.status_label is not None

@pytest.mark.asyncio
async def test_get_response(ai_tab: AITab, ai_system: AsyncMock, qtbot):
    ai_system.get_response.return_value = 'response'
    ai_tab.prompt_input.setText('prompt')
    qtbot.mouseClick(ai_tab.submit_button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: ai_tab.response_output.toPlainText() == 'response', timeout=5000)
    assert ai_tab.response_output.toPlainText() == 'response'
    assert ai_tab.status_label.text() == 'Response received successfully.'
def test_show_error_message(ai_tab: AITab, qtbot):
    with qtbot.waitSignal(ai_tab.status_label.textChanged):
        ai_tab.show_error_message('Error message')
    assert ai_tab.status_label.text() == 'Error message'

def test_show_success_message(ai_tab: AITab, qtbot):
    with qtbot.waitSignal(ai_tab.status_label.textChanged, timeout=5000):
        ai_tab.show_success_message('Success message')
    assert ai_tab.status_label.text() == 'Success message'

def test_clear_input(ai_tab: AITab, qtbot):
    ai_tab.prompt_input.setText('prompt')
    with qtbot.waitSignal(ai_tab.prompt_input.textChanged):
        ai_tab.clear_input()
    assert ai_tab.prompt_input.text() == ''
    assert ai_tab.response_output.toPlainText() == ''
    assert ai_tab.status_label.text() == ''
    with qtbot.waitExposed(ai_tab.loading_indicator):
        ai_tab.set_loading_state(True)
    assert ai_tab.loading_indicator.isVisible()
    assert not ai_tab.submit_button.isEnabled()
    with qtbot.waitExposed(ai_tab.loading_indicator, visible=False):
        assert not ai_tab.loading_indicator.isVisible()
    assert not ai_tab.loading_indicator.isVisible()
    assert not ai_tab.loading_indicator.isVisible()

def test_validate_input(ai_tab: AITab):
    assert not ai_tab.validate_input('')
    assert ai_tab.validate_input('prompt')
