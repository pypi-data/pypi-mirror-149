'''The comm_layer_type doesnt matter here. All agents will use the raw type
'''

import contextlib
import platform

import pytest # type: ignore

from arps.core.real.agents_directory_helper import AgentsDirectoryHelper
from arps.core.real.rest_api_utils import HTTPMethods, invoke_rest_ws
from arps.test_resources.apps_runner import (start_agents_directory,
                                             start_agent_manager)
from arps.test_resources.configuration_template import generate_real_env_configuration


def test_agents_manager_add_successfully():
    with contextlib.ExitStack() as stack:
        agents_directory_port = stack.enter_context(start_agents_directory())
        agents_directory = {'address': platform.node(),
                            'port': agents_directory_port}

        agent_config = ["arps", "test_resources", "conf", "dummy_agent.conf"]

        conf_file_name = stack.enter_context(generate_real_env_configuration(agent_config,
                                                                             agents_directory,
                                                                             'raw'))

        agents_directory = AgentsDirectoryHelper(**agents_directory)

        assert not agents_directory.list()

        user_defined_parameters = ['--config_file', conf_file_name]
        agent_manager_accessor = stack.enter_context(start_agent_manager(user_defined_parameters))

        content = agents_directory.list()
        assert content

        am_content, response = invoke_rest_ws(HTTPMethods.GET,
                                              agent_manager_accessor('about'))
        assert response.code == 200
        assert f"{am_content['identifier']}.0" in content


def test_fail_agent_manager_when_there_is_no_agents_directory_running():
    agent_config = ["arps", "test_resources", "conf", "dummy_agent.conf"]
    address, port = platform.node(), 1
    agents_directory = {'address': address, 'port': port} # Doesn't matter
    with generate_real_env_configuration(agent_config, agents_directory, 'raw') as conf_file_name:
        user_defined_parameters = ['--config_file', conf_file_name]
        with pytest.raises(RuntimeError) as excinfo:
            with start_agent_manager(user_defined_parameters):
                pass
        assert str(excinfo.value).startswith(f'Error: Error while accessing resource http://{address}:{port}/agents')


def test_fail_agent_manager_when_there_is_already_a_registered_identifier():
    with contextlib.ExitStack() as stack:
        agents_directory_port = stack.enter_context(start_agents_directory())
        agents_directory = AgentsDirectoryHelper(address=platform.node(),
                                                 port=agents_directory_port)

        # adding just to test if the service is working as expected
        result = agents_directory.add(agent_id='0.0',
                                      address='dummy_hostname',
                                      port=None)
        assert result == 'Agent 0.0 added'

        result = agents_directory.list()
        assert '0.0' in result

        agent_config = ["arps", "test_resources", "conf", "dummy_agent.conf"]
        agents_directory = {'address': platform.node(), 'port': agents_directory_port}

        conf_file_name = stack.enter_context(generate_real_env_configuration(agent_config,
                                                                             agents_directory,
                                                                             'raw'))

        user_defined_parameters = ['--config_file', conf_file_name]
        with pytest.raises((RuntimeError, TimeoutError)) as excinfo:
            with start_agent_manager(user_defined_parameters):
                pass

        expected_message = 'Error: Agent 0.0 is already added but with different parameters.'

        # The message is long. Opted to use only portion of it to validate the test
        assert expected_message in str(excinfo.value)

if __name__ == '__main__':
    pytest.main([__file__])
