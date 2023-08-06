import platform
import pathlib
import subprocess
import re

import pytest # type: ignore

from arps.core.real.rest_api_utils import random_port

from arps.test_resources.agent_runner_helper import setup_environment


RESPONSE_PATTERN = re.compile('policies=(.*),')
TOUCHPOINT_PATTERN = re.compile('touchpoint=({.*})')

def check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper):
    assert proc_status[0], proc_status
    assert agent_proc.poll() is None

    result = agents_directory_helper.list()
    assert '0.0' in result, f'agent {agent_port}, ad port {agents_directory_helper.port}, status {agent_proc.communicate()}'

    agent = result['0.0']
    assert 'address' in agent and agent['address'] is not None
    assert agent['port'] == str(agent_port)


def check_loaded_policies_using_agent_client(comm_layer_type, ad_port, *args):
    result = subprocess.run(['agent_client',
                             '--id', '0', '1',
                             '--comm_layer', comm_layer_type,
                             '--agent', '0.0',
                             '--agents_directory', f'{platform.node()}', f'{ad_port}',
                             '--request_type', 'info'],
                            stdout=subprocess.PIPE,
                            check=True).stdout
    response = result.decode()
    policies = eval(RESPONSE_PATTERN.search(response).group(1))

    expected_policies = ['InfoProviderPolicy', 'TouchPointStatusProviderPolicy', 'MetaPolicyProvider', 'MetaAgentProviderPolicy']
    expected_policies.extend(args)
    assert sorted(expected_policies) == sorted(policies)


def check_sensors_using_agent_client(comm_layer_type, ad_port):
    result = subprocess.run(['agent_client',
                             '--id', '0', '1',
                             '--comm_layer', comm_layer_type,
                             '--agent', '0.0',
                             '--agents_directory', f'{platform.node()}', f'{ad_port}',
                             '--request_type', 'sensors'],
                            stdout=subprocess.PIPE,
                            check=True).stdout
    response = result.decode()
    touchpoint = eval(TOUCHPOINT_PATTERN.search(response).group(1))
    assert touchpoint['ResourceA'] == 40
    assert touchpoint['ResourceB'] == 'ON'
    # since it's using actual agents to run, it expected the resource
    # to be real as well
    assert touchpoint['DummyResource'] == 'RealResource'


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_regular_policy(comm_layer_type):
    agent_port = random_port()

    policy = 'DummyPolicy'
    user_parameters = ['--policy',
                       policy,
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy)
        check_sensors_using_agent_client(comm_layer_type, agents_directory_helper.port)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_periodic_policy(comm_layer_type):
    agent_port = random_port()

    policy = 'DummyPeriodicPolicy'
    user_parameters = ['--periodic_policy',
                       'DummyPeriodicPolicy', '1',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_mix_policies(comm_layer_type):
    agent_port = random_port()

    policy1 = 'DummyPolicy'
    policy2 = 'DummyPeriodicPolicy'
    user_parameters = ['--policy',
                       policy1,
                       '--periodic_policy',
                       policy2, '1',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy1, policy2)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_multiple_regular_policies(comm_layer_type):
    agent_port = random_port()

    policy1 = 'DummyPolicy'
    policy2 = 'ReceiverPolicy'
    user_parameters = ['--policy',
                       policy1,
                       '--policy',
                       policy2,
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy1, policy2)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_multiple_periodic_policies(comm_layer_type):
    agent_port = random_port()

    policy1 = 'DummyPeriodicPolicy'
    policy2 = 'SenderPolicy'
    user_parameters = ['--periodic_policy',
                       policy1, '1',
                       '--periodic_policy',
                       policy2, '2',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy1, policy2)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_user_defined_mix_multiple_policies(comm_layer_type):
    agent_port = random_port()

    policy1 = 'DummyPolicy'
    policy2 = 'ReceiverPolicy'
    policy3 = 'DummyPeriodicPolicy'
    policy4 = 'SenderPolicy'
    user_parameters = ['--policy', policy1,
                       '--policy', policy2,
                       '--periodic_policy', policy3, '1',
                       '--periodic_policy', policy4, '2',
                       '--config_file', pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, agent_port) as ((proc_status, agent_proc), agents_directory_helper):
        check_if_agent_is_available(proc_status, agent_proc, agent_port, agents_directory_helper)
        check_loaded_policies_using_agent_client(comm_layer_type, agents_directory_helper.port, policy1, policy2, policy3, policy4)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_periodic_policy(comm_layer_type):
    user_parameters = ['--periodic_policy',
                       'ResourceAMonitorPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert 'agent_runner: error: argument --periodic_policy: expected 2 arguments' == status[1].splitlines()[-1]
        assert 2 == agent_proc.returncode

        assert not agents_directory_helper.list()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_repeated_policy(comm_layer_type):
    user_parameters = ['--policy',
                       'DummyPolicy',
                       '--policy',
                       'DummyPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert 'Only one instance of a policy is allowed. Check if a policy is being added more than once' == status[1]
        assert 1 == agent_proc.returncode

        assert not agents_directory_helper.list()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_misconfigured_user_defined_module_file(comm_layer_type):
    user_parameters = ['--policy',
                       'DummyPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent_with_error_in_user_modules.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert "No module named 'arps.test_resources.non_existent_module', check if module or attribute name exists" == status[1]
        assert 1 == agent_proc.returncode

        assert not agents_directory_helper.list()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_misconfigured_resources(comm_layer_type):
    user_parameters = ['--policy',
                       'DummyPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent_with_error_in_resources.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert "module 'arps.test_resources.dummies.resources' has no attribute 'InvalidResource', check attribute name" == status[1]
        assert 1 == agent_proc.returncode

        assert not agents_directory_helper.list()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_misconfigured_touchpoints(comm_layer_type):
    user_parameters = ['--policy',
                       'DummyPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent_with_error_in_touchpoints.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert "module 'arps.test_resources.dummies.touchpoints' has no attribute 'InvalidSensor', check attribute name" == status[1]
        assert 1 == agent_proc.returncode

        assert not agents_directory_helper.list()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_agent_creation_failure_misconfigured_policies(comm_layer_type):
    user_parameters = ['--policy',
                       'DummyPolicy',
                       '--config_file',
                       pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent_with_error_in_policies.conf',
                       '--comm_layer', comm_layer_type]

    with setup_environment(user_parameters, random_port()) as ((status, agent_proc), agents_directory_helper):
        assert not status[0], status
        assert "module 'arps.test_resources.dummies.policies' has no attribute 'InvalidPolicy', check attribute name" == status[1]
        assert 1 == agent_proc.returncode

        assert not agents_directory_helper.list()


if __name__ == '__main__':
    pytest.main([__file__])
