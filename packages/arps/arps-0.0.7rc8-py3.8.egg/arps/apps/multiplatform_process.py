'''This module has the functions to create and terminate process using
subprocess module regardless if it is Windows or Linux.
'''

import subprocess
import platform
import signal
import os

from arps.core.real.rest_api_utils import wait_for_process

def create_process(*args, **kwargs):
    '''Creates subprocess with CREATE_NEW_PROCESS_GROUP in Windows to
    enable the process to receive signals
    '''
    if platform.system() == 'Windows':
        kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP

    proc = subprocess.Popen(*args, **kwargs)

    try:
        wait_for_process(proc)

        return (True, 'Process {} created successfully'.format(proc.pid)), proc
    except (RuntimeError, TimeoutError) as err:
        proc.terminate() #just to be sure
        return (False, str(err)), proc

def terminate_process(process, timeout=10):
    '''Send signal to terminate process

    Returns return code 0 if the process terminates successfully, another exit code along with the error message otherwise

    Args:
    - process: instance of subprocess.Popen
    - timeout: timeout for waiting process until it finishes

    Warning: this is meant to be used together with
    create_process. For example, in Windows, terminate_process on a
    process created without the proper creationflags will result in
    failure.

    '''
    if platform.system() == 'Windows':
        os.kill(process.pid, signal.CTRL_BREAK_EVENT)
    else:
        process.send_signal(signal.SIGINT)

    try:
        process.wait(timeout)

        return process.returncode, 'Process {} terminated'.format(process.pid)
    except subprocess.TimeoutExpired as error:
        process.terminate()
        return process.returncode, str(error)
