from .module import MainClass

# src/__init__.py
from src.config.config import Config
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize Config
config = Config()