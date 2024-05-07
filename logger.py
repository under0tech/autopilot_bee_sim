import logging
import definitions as vars
from datetime import datetime

def init_logger():
    logger = logging.getLogger(vars.logger_name)
    logger.setLevel(logging.DEBUG)
    log_file_handler = logging.FileHandler(
        f'logs/log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)
    return logger

bee_logger = init_logger()

def log_message(logger, message, level='debug'):
    if level == 'debug':
        bee_logger.debug(message)
    elif level == 'info':
        bee_logger.info(message)
    elif level == 'warning':
        bee_logger.warning(message)
    elif level == 'error':
        bee_logger.error(message)
    elif level == 'fatal':
        bee_logger.fatal(message)
    else:
        raise ValueError(
            "Invalid logging level. Choose from 'debug', \
'info', 'warning', 'error', or 'fatal'.")