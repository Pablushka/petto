import logging
import sys
from config import settings


def setup_logging():
    """Configure application logging with appropriate levels for environment"""
    
    # Set log level based on environment
    if settings.environment == "production":
        level = logging.INFO
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        level = logging.DEBUG
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Suppress noisy third-party logs in production
    if settings.environment == "production":
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("tortoise").setLevel(logging.WARNING)
        logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


# Create a security-specific logger
def get_security_logger():
    """Get a logger specifically for security events"""
    logger = logging.getLogger("security")
    
    # Security events should always be logged
    logger.setLevel(logging.INFO)
    
    # Create security log handler if it doesn't exist
    if not logger.handlers:
        security_handler = logging.FileHandler("security.log")
        security_formatter = logging.Formatter(
            "%(asctime)s - SECURITY - %(levelname)s - %(message)s"
        )
        security_handler.setFormatter(security_formatter)
        logger.addHandler(security_handler)
        logger.propagate = False  # Don't duplicate to main log
    
    return logger


# Initialize logging
app_logger = setup_logging()
security_logger = get_security_logger()