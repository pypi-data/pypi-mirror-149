import subprocess
import functools
import contextlib
import traceback
import platform
import os
import logging
import pathlib

import psutil  # type: ignore

from arps.core.real.rest_api_utils import (try_to_connect,
                                           build_url,
                                           wait_for_process,
                                           random_port)

from arps.apps.multiplatform_process import terminate_process


def remove_process_files(pid):
    logger = logging.getLogger()
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        logger.warning('No such process %s', pid)
        return

    files = [pathlib.Path(pfile.path) for pfile in process.open_files()]
    files = [pfile for pfile in files if pfile.suffix == '.log']
    for f in files:
        try:
            print('Removing', f)
            os.remove(f)
        except PermissionError:
            logger.warning('Permission error when removing file %s: %s',
                           f, exec_info=True)
        except FileNotFoundError:
            logger.warning('File not found error when removing file %s: %s',
                           f, exec_info=True)
        except OSError as err:
            logger.warning(err, exec_info=True)


@contextlib.contextmanager
def start_agent_manager(user_defined_parameters, quiet=True, debug=False):
    '''Start agent manager with user defined parameters, except port
    which is handled here

    It yields the resource endpoint partially built

    See agent_manager_runner argparse for more information about parameters.

    Args:
    - user_defined_parameters: parameters supported by agent_manager_runner
    - quiet: if true, does not generate any log
    - debug: if true, generates some statistics
    '''

    subprocess_popen = ['agent_manager_runner']
    subprocess_popen.extend(user_defined_parameters)

    port = random_port()

    subprocess_popen.extend(['--port', str(port)])
    if quiet:
        subprocess_popen.append('--quiet')

    if debug:
        subprocess_popen.append('--debug')

    with subprocess.Popen(subprocess_popen,
                          stderr=subprocess.PIPE,
                          stdout=subprocess.PIPE) as agent_manager:
        process_files = []
        children_files = []
        try:
            wait_for_process(agent_manager)  # can raise RuntimeError or TimeoutError

            if try_to_connect(tries=5, port=port):
                yield functools.partial(build_url,
                                        f'{platform.node()}:{port}')

            if quiet:
                process_files = psutil.Process(agent_manager.pid).open_files()
                children_pids = [pc.pid for pc in psutil.Process(agent_manager.pid).children()]
                for pc in children_pids:
                    children_files.extend(psutil.Process(pc).open_files())
                print('children files', str(children_files))

            terminate_process(agent_manager)
            agent_manager.wait(timeout=5)
        except (RuntimeError, TimeoutError, subprocess.TimeoutExpired) as err:
            agent_manager.terminate()
            raise RuntimeError(str(err))
        except AssertionError:
            raise
        except Exception as err:
            print('Something unexpected happened', err)
            print('Exception type happened', type(err))
            print('traceback', traceback.format_exc())
        finally:
            if agent_manager.returncode is None:
                agent_manager.terminate()

            if quiet:
                # removing children files after the process is done to
                # avoid any issues
                children_files = [f for f in children_files if f.path.endswith('.log')]

                for child_file in children_files:
                    with contextlib.suppress(PermissionError, FileNotFoundError, OSError):
                        print('removing', child_file.path)
                        os.remove(child_file.path)

                process_files = [f for f in process_files if f.path.endswith('.log')]
                for process_file in process_files:
                    with contextlib.suppress(PermissionError, FileNotFoundError, OSError):
                        print('removing', process_file.path)
                        os.remove(process_file.path)

            print('agent manager terminated {}'.format(agent_manager.returncode))


@contextlib.contextmanager
def start_pmt_service():
    # This service is optional. The code is here just to make it easy
    # to start it if necessary
    pmt_port = random_port()
    pmt_popen = ['pmt_service', '--port', str(pmt_port)]
    with subprocess.Popen(pmt_popen) as pmt:
        wait_for_process(pmt, timeout=30)
        assert try_to_connect(port=pmt_port)

        try:
            yield pmt_port

            remove_process_files(pmt.pid)
            terminate_process(pmt)
            pmt.wait(5)
        except (RuntimeError, TimeoutError, subprocess.TimeoutExpired) as err:
            raise RuntimeError(err)
        except AssertionError:
            raise
        except Exception as err:
            print('Something unexpected happened', err)
            print('Exception type happened', type(err))
            print('traceback', traceback.format_exc())
        finally:
            if pmt.returncode is None:
                pmt.terminate()
            print('pmt service terminated {}'.format(pmt.returncode))


@contextlib.contextmanager
def start_agents_directory():
    agents_directory_port = random_port()
    agents_directory_popen = ['agents_directory']

    agents_directory_popen.extend(['--port', str(agents_directory_port)])
    agents_directory_popen.append('--quiet')
    with subprocess.Popen(agents_directory_popen) as agents_directory:
        try:
            wait_for_process(agents_directory)
            if try_to_connect(port=agents_directory_port, tries=5):
                yield agents_directory_port

            remove_process_files(agents_directory.pid)
            terminate_process(agents_directory)
            agents_directory.wait(5)
        except (RuntimeError, TimeoutError, subprocess.TimeoutExpired) as err:
            print('Error while running agents directory', err)
            raise RuntimeError(err)
        except AssertionError:
            raise
        except Exception as err:
            print('Something unexpected happened', err)
            print('Exception type happened', type(err))
            print('traceback', traceback.format_exc())
        finally:
            if agents_directory.returncode is None:
                agents_directory.terminate()
            print('agents directory service terminated {}'.format(agents_directory.returncode))
