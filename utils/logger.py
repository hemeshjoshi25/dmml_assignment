import logging

from configs.config import LOG_PATH

# Create logs directory if it doesn't exist
LOG_PATH.mkdir(parents=True, exist_ok=True)


def get_logger(log_file_name):
    """
    Creates and returns a logger instance.

    Parameters:
        log_file_name (str): Name of the log file.

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(log_file_name)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    file_handler = logging.FileHandler(LOG_PATH / log_file_name)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger