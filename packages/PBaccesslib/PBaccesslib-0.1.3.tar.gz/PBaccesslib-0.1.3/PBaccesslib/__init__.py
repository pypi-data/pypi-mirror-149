import os
import logging.handlers
from K2600acceslib import log_to_screen as k2600_screen, log_add_file_handler as k2600_add_file
from Commacceslib import log_to_screen as comm_screen, log_add_file_handler as comm_add_file


input_data_path = os.path.abspath(os.path.dirname(__file__))
BITMAP = 0x1
VERBOSE = True
CHIP_REG_PATH = os.path.join(input_data_path, 'data', 'chip_reg.npy')
PIXEL_REG_PATH = os.path.join(input_data_path, 'data', 'pixel_reg.npy')
LOG_FILE_PATH = os.path.join(input_data_path, 'data', 'logg.txt')

# Defined here since it is imported in other pyvisa modules
BASE_NAME = 'ProbeCard'
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def log_to_screen(level=logging.DEBUG) -> None:
    log_to_stream(None, level)  # sys.stderr by default


def log_to_stream(stream_output, level=logging.DEBUG) -> None:
    logger.setLevel(level)
    ch = logging.StreamHandler(stream_output)
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def log_add_file_handler(file_path, level=logging.DEBUG):
    fh = logging.handlers.RotatingFileHandler(filename=file_path, maxBytes=5 * 1024 * 1024, backupCount=5)
    fh.setLevel(level=level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def std_file_on(file_path):
    """ Add data to file """
    log_add_file_handler(file_path)
    k2600_add_file(file_path)
    comm_add_file(file_path)

    """ Std out log """
    log_to_screen()
    k2600_screen()
    comm_screen()


if VERBOSE:
    std_file_on(LOG_FILE_PATH)

__version__ = "unknown"

__all__ = [
    "logger",
    "log_to_screen",
    "log_to_stream",
    "log_add_file_handler",
    "BITMAP",
    "LOG_FILE_PATH",
    "CHIP_REG_PATH",
    "PIXEL_REG_PATH",
]
