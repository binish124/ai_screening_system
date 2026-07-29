import logging
import os

# Ensure a logs directory exists at the root of the project
os.makedirs("logs", exist_ok=True)

def setup_logger(name):
    """
    Sets up a logger that outputs to both the console and a log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console Handler (shows INFO and above in the terminal)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)

    # File Handler (saves DEBUG and above to the log file)
    f_handler = logging.FileHandler('logs/ai_system.log')
    f_handler.setLevel(logging.DEBUG)

    # Define the standardized log format
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger