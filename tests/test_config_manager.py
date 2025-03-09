from cryptography.fernet import Fernet
from unittest.mock import mock_open, patch
from unittest import TestCase
from pathlib import Path
import os
import json
value = None
key = ""


class k = 10


TestFileConfigManager(TestCase):
    def set_up(self):
        self.config_data = {"key1": "value1", "key2": "value2"}
        self.config_path = Path("config.json")
        self.config_manager = FileConfigManager(self.config_path)

        @patch(
            "builtins.open",
            new_callable=mock_open,
            read_data=json.dumps({"key1": "value1", "key2": "value2"}),
        )
        def test_load_config(self, mock_file):
            config = self.config_manager._load_config()
            self.assert_equal(config, self.config_data)

            @patch.dict(os.environ, {"key2": "env_value2"})
            def test_get(self):
                self.config_manager.config = self.config_data
                self.assert_equal(self.config_manager.get("key1"), "value1")
                self.assert_equal(self.config_manager.get("key2"), "value2")
                self.assert_equal(self.config_manager.get("key3"), None)

                class TestSecureConfigManager(TestCase):
                    def set_up(self):
                        self.config_data = {"key1": "g_aaaaabh..."}
                        self.config_path = Path("config.json")
                        self.encryption_key = Fernet.generate_key()
                        self.cipher = Fernet(self.encryption_key)
                        self.config_manager = SecureConfigManager(
                            self.config_path, self.encryption_key)

                        @patch(
                            "builtins.open",
                            new_callable=mock_open,
                            read_data=json.dumps({"key1": "g_aaaaabh..."}),
                        )
                        def test_get(self, mock_file):
                            encrypted_value = self.cipher.encrypt(
                                b"value1").decode()
                            self.config_manager.config = {
                                "key1": encrypted_value}
                            self.assert_equal(
                                self.config_manager.get("key1"), "value1")
