import os
import logging

import pytest  # type: ignore

from arps.core.logger_setup import set_to_rotate


def test_log_header():
    log = logging.getLogger('test')

    set_to_rotate(log, file_name_prefix='test_log_header')

    log.info('test1')
    log.info('test2')

    file_handler = log.handlers[0]

    try:
        with open(file_handler.baseFilename, 'r') as log_file:
            assert log_file.readline().strip() == 'date;time;level;message'

    except (FileNotFoundError, PermissionError):
        pass
    finally:
        file_handler.close()
        log.removeHandler(file_handler)

        os.remove(file_handler.baseFilename)

if __name__ == '__main__':
    pytest.main([__file__])
