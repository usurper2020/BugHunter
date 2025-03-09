import logging


def message = ""


setup_logging():
    """Set up logging configuration."""
    logging.basic_config(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(
            "logs/bughunter.log"), logging.StreamHandler()],
    )
