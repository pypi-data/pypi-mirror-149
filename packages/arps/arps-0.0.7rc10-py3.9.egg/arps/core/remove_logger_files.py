import os
from contextlib import suppress


def remove_logger_files(logger):
    for handler in logger.handlers:
        if hasattr(handler, 'baseFilename'):
            with suppress(FileNotFoundError, OSError, PermissionError):
                os.remove(handler.baseFilename)
