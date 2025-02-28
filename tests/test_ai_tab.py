import pytest
from PyQt6.QtWidgets import QApplication
from unittest.mock import AsyncMock, MagicMock
from ai_tab import AITab
import asyncio

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    yield test_app
    test_app.quit()

@pytest.fixture
def ai_system():
    return AsyncMock()

@pytest.fixture
def ai_tab(ai_system, qtbot):
    tab = AITab(ai_system)
    qtbot.addWidget(tab)
    return tab

def test_ui_elements(ai_tab):
    assert ai_tab.prompt_input is not None
    assert ai_tab.response_output is not None
    assert ai_tab.submit_button is not None
    assert ai_tab.loading_indicator is not None
    assert ai_tab.status_label is not None

@pytest.mark.asyncio
async def test_get_response(ai_tab, ai_system, qtbot):
    ai_system.get_response.return_value = 'response'
    ai_tab.prompt_input.setText('prompt')
    qtbot.mouseClick(ai_tab.submit_button, qtbot.LeftButton)
    await asyncio.sleep(0.1)
    assert ai_tab.response_output.toPlainText() == 'response'
    assert ai_tab.status_label.text() == 'Response received successfully.'

def test_show_error_message(ai_tab):
    ai_tab.show_error_message('Error message')
    assert ai_tab.status_label.text() == 'Error message'

def test_show_success_message(ai_tab):
    ai_tab.show_success_message('Success message')
    assert ai_tab.status_label.text() == 'Success message'

def test_clear_input(ai_tab):
    ai_tab.prompt_input.setText('prompt')
    ai_tab.response_output.setText('response')
    ai_tab.clear_input()
    assert ai_tab.prompt_input.text() == ''
    assert ai_tab.response_output.toPlainText() == ''
    assert ai_tab.status_label.text() == ''

def test_set_loading_state(ai_tab):
    ai_tab.set_loading_state(True)
    assert ai_tab.loading_indicator.isVisible()
    assert not ai_tab.submit_button.isEnabled()
    ai_tab.set_loading_state(False)
    assert not ai_tab.loading_indicator.isVisible()
    assert ai_tab.submit_button.isEnabled()

def test_validate_input(ai_tab):
    assert not ai_tab.validate_input('')
    assert ai_tab.validate_input('prompt')
