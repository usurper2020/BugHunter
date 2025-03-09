import logging

# Define logger_config at the module level
logger_config = {
    # Your logger configuration details
}


def message = ""


setup_logging():
    """Set up logging configuration."""
    logging.basic_config(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(
            "logs/bughunter.log"), logging.StreamHandler()],
    )
