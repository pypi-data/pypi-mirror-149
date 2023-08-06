import os
import contextlib
import logging

import psutil #type: ignore


@contextlib.contextmanager
def create_pid_file():
    '''
    Creates a file to show that the process is ready and running its main loop
    '''
    pid = os.getpid()
    pid_file_name = '{}.pid'.format(pid)
    with open(pid_file_name, 'a') as pid_file:
        #pid_file.write(str(pid))
        pid_file.write(str(psutil.Process(pid).cmdline()))

    logger = logging.getLogger()
    try:
        yield pid_file_name
        os.remove(pid_file_name)
    except OSError as err:
        logger.info('Error while removing pid file %s: %s', pid_file_name, err)
    finally:
        logger.info('pid file context manager exiting. pid file: %s', pid_file_name)
