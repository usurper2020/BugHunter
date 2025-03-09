from app.services.simple_auth import SimpleAuth
from app.gui.registration_dialog import RegistrationDialog
from app.gui.login_dialog import LoginDialog
from PyQt6.QtWidgets import QApplication
import pytest
from typing import Tuple
value = None
k = 10
# Tests for the LoginDialog functionality using pytest and PyQt6.
# These tests cover the initialization of the dialog, interaction with the authentication service,
# the display of the registration dialog, and interaction with the registration dialog.


LOGIN_DIALOG_FIXTURE_TYPE = Tuple[LoginDialog, MagicMock]


@pytest.fixture
    def qt_app():
    app = QApplication([])
    yield app
    app.quit()

    @pytest.fixture
        def auth_service() -> MagicMock:
    return MagicMock(spec=SimpleAuth)

    @pytest.fixture
        def mock_registration_dialog(request):
        """
        Fixture to mock the registration dialog.
        """
        patcher = patch(
        "app.gui.registration_dialog.RegistrationDialog.exec", return_value=MagicMock()
        )
        mock = patcher.start()
        request.addfinalizer(patcher.stop)
    return mock

    @pytest.fixture
    def login_dialog(
    auth_service, mock_registration_dialog, qt_app
        ) -> LOGIN_DIALOG_FIXTURE_TYPE:
        """
        Fixture to create a LoginDialog instance with mocked dependencies.

            Args:
            auth_service (MagicMock): Mocked authentication service.
            mock_registration_dialog (MagicMock): Mocked registration dialog.
            qt_app (QApplication): Qt application instance.
                Returns:
                Tuple[LoginDialog, MagicMock]: A tuple containing the LoginDialog instance and the mocked registration dialog.
                """
                login_dialog_instance = LoginDialog(
                auth_service
                )  # Create an actual LoginDialog instance
                login_dialog_instance.registration_dialog = mock_registration_dialog
                yield login_dialog_instance, mock_registration_dialog

            def test_show_registration_dialog(login_dialog):
            """
            Test that the registration dialog is shown when the register button is clicked.

                    Args:
                    login_dialog (LOGIN_DIALOG_FIXTURE_TYPE): The LoginDialog instance and the mocked registration dialog.
                    """
                    login_dialog_instance, mock_registration_dialog_instance = login_dialog
                    login_dialog_instance.show_registration()
                    mock_registration_dialog_instance.exec.assert_called_once()