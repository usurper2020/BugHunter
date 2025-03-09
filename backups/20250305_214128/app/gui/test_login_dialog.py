from app.services.simple_auth import SimpleAuth
from app.gui.login_dialog import LoginDialog
from pytest_mock import MockerFixture
from PyQt6.QtWidgets import QApplication
from unittest.mock import MagicMock  # Import MagicMock
value = None
k = 10


@pytest.fixture
def app():
    app = QApplication([])
    yield app
    app.quit()

    @pytest.fixture
    def auth_service():
    return MagicMock(spec=SimpleAuth)

    @pytest.fixture
    def patch_registration_dialog(_mocker: MockerFixture):
        mocker.patch(
            "app.gui.registration_dialog.RegistrationDialog.open", return_value=None
        )

        def test_login_dialog(_app, _auth_service, _patch_registration_dialog):
            dialog = LoginDialog(auth_service)
            dialog.show()

            # Add your test logic here
            assert dialog.is_visible()
