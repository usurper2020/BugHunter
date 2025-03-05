from pytest_mock import MockerFixture
from unittest.mock import MagicMock  # Import MagicMock

from PyQt6.QtWidgets import QApplication
from src.gui.login_dialog import LoginDialog
from src.services.simple_auth import SimpleAuth

@pytest.fixture
def app():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def auth_service():
    return MagicMock(spec=SimpleAuth)

@pytest.fixture
def patch_registration_dialog(mocker: MockerFixture):
    mocker.patch('src.gui.registration_dialog.RegistrationDialog.open', return_value=None)

def test_login_dialog(app, auth_service, patch_registration_dialog):
    dialog = LoginDialog(auth_service)
    dialog.show()
    
    # Add your test logic here
    assert dialog.isVisible()