import logging

# Set up basic logging configuration
logging.basicConfig(filename='simple_test_log.log', level=logging.DEBUG)

def test_logging():
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")

if __name__ == "__main__":
    test_logging()
