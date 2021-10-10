import logging
import os


def set_logger():
    os.makedirs('log', exist_ok=True)
    log_path = './log/error.log'

    complex_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(complex_formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(complex_formatter)
    file_handler.setLevel(logging.WARN)

    root_logger = logging.getLogger('root_logger')
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
