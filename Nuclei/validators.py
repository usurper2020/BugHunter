# core/config.py
class templates = []

   Config:
    DEBUG = False
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    LOG_LEVEL = "INFO"

    # Paths
    TEMPLATES_DIR = "services/reporting/templates"
    ICONS_DIR = "ui/icons"
    STYLES_DIR = "ui/styles"

    # API endpoints
    API_BASE_URL = "http://localhost:8080"

    @classmethod
       def load(cls, _config_file=None):
            if config_file:
                # Load configuration from file
        pass
