import subprocess
import contextlib
import platform

from arps.core.real.agents_directory_helper import AgentsDirectoryHelper
from arps.apps.multiplatform_process import create_process, terminate_process

from arps.test_resources.apps_runner import (start_agents_directory,
                                             remove_process_files)


@contextlib.contextmanager
def setup_environment(user_parameters, agent_port):
    with start_agents_directory() as agents_directory_port:
        agents_directory_helper = AgentsDirectoryHelper(address=platform.node(),
                                                        port=agents_directory_port)

        popen = ['agent_runner',
                 '--id', '0', '0',
                 '--port', str(agent_port),
                 '--agents_dir_addr', 'localhost',
                 '--agents_dir_port', str(agents_directory_port)]
        popen.extend(user_parameters)

        proc_status, agent_proc = create_process(popen, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        yield (proc_status, agent_proc), agents_directory_helper

        remove_process_files(agent_proc.pid)
        terminate_process(agent_proc)

        try:
            agent_proc.wait(5)
        except subprocess.TimeoutExpired as error:
            agent_proc.terminate()
            assert False, str(error)
        finally:
            print('agent terminated {}'.format(agent_proc.returncode))
