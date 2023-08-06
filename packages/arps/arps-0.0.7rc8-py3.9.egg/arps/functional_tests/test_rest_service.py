import contextlib
import io
import pathlib
import platform
from collections import Counter
from functools import partial
from http import HTTPStatus
from time import sleep

import pytest  # type: ignore

from arps.core.real.rest_api_utils import (
    HTTPMethods,
    build_http_body_and_header,
    invoke_rest_ws,
)
from arps.test_resources.apps_runner import start_agent_manager, start_agents_directory
from arps.test_resources.configuration_template import generate_real_env_configuration

# To generate the logs pass the parameter "quiet=False" to
# start_agent_manager

# pylint:disable=redefined-outer-name
# noqa: W503


@contextlib.contextmanager
def sim_environment():
    user_defined_parameters = [
        '--config_file',
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment_random_events.conf',
    ]
    try:
        with start_agent_manager(user_defined_parameters) as endpoint:
            content, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/run'))
            assert content
            assert response.code == HTTPStatus.OK

            yield endpoint

            content, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/run'))
            assert content
            assert response.code == HTTPStatus.OK
    except RuntimeError as err:
        print(err)


def test_sim_precondition_sim_running():
    user_defined_parameters = [
        '--config_file',
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment_random_events.conf',
    ]

    try:
        with start_agent_manager(user_defined_parameters) as endpoint:
            spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

            url = endpoint('0/agents/0.1?request_type=sensors')
            content, response = invoke_rest_ws(HTTPMethods.GET, url)
            assert response.code == HTTPStatus.BAD_REQUEST
            assert (
                response.reason
                == 'epoch not running, start it by running the simulator '
                'before invoking this command'
            )
            assert not content
    except RuntimeError as err:
        print(err)


def test_multiple_agent_manager():
    with sim_environment() as endpoint:
        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('about'))
        assert response.code == HTTPStatus.OK
        assert result['simulation']
        assert len(result['agent_managers']) == 2
        assert 0 in result['agent_managers']
        assert 1 in result['agent_managers']

        body, headers = build_http_body_and_header(
            {'policies': {'DummyPolicyWithBehavior': 1}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, endpoint('0/agents'), body, headers
        )
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 0.1 created'

        body, headers = build_http_body_and_header({'policies': {'DummyPolicy': None}})
        result, response = invoke_rest_ws(
            HTTPMethods.POST, endpoint('1/agents'), body, headers
        )
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 1.1 created'

        result, response = invoke_rest_ws(
            HTTPMethods.GET, endpoint('0/agents/0.1?request_type=sensors')
        )
        assert response.code == HTTPStatus.OK
        assert Counter(result['content']['touchpoint'].keys()) == Counter(
            ['ResourceA', 'ResourceB', 'DummyResource']
        )

        result, response = invoke_rest_ws(
            HTTPMethods.GET, endpoint('1/agents/1.1?request_type=sensors')
        )
        assert response.code == HTTPStatus.OK
        assert Counter(result['content']['touchpoint'].keys()) == Counter(
            ['ResourceA', 'ResourceB']
        )


def test_request_monitor_log_when_there_are_no_monitor_logs(endpoint):
    assert_failure_monitor_log_request(endpoint)


def test_request_monitor_log_when_there_are_agents_but_no_monitor_logs(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    assert_failure_monitor_log_request(endpoint)


def test_monitor_logs_after_the_simulation_is_done():
    with sim_environment() as endpoint:
        body, headers = build_http_body_and_header(
            {'policies': {'ResourceAMonitorPolicy': 1}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, endpoint('agents'), body, headers
        )
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 0.1 created'

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/run'))
        assert result == 'running'
        assert response.code == HTTPStatus.OK

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
        while result == 'running':
            result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
            assert response.code == HTTPStatus.OK
            sleep(0.15)

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        assert_header_monitor_log('date,time,ResourceA', endpoint)


def test_monitor_logs_after_the_simulation_is_done_and_the_agent_is_terminated():
    with sim_environment() as endpoint:
        body, headers = build_http_body_and_header(
            {'policies': {'ResourceAMonitorPolicy': 1}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, endpoint('agents'), body, headers
        )
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 0.1 created'

        body, headers = build_http_body_and_header(
            {'policies': {'ResourceBMonitorPolicy': 1}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, endpoint('agents'), body, headers
        )
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 0.2 created'

        result, response = invoke_rest_ws(HTTPMethods.DELETE, endpoint('agents/0.1'))
        assert response.code == HTTPStatus.OK
        assert result == 'Agent 0.1 terminated successfully'

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/run'))
        assert result == 'running'
        assert response.code == HTTPStatus.OK

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
        while result == 'running':
            result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
            assert response.code == HTTPStatus.OK
            sleep(0.15)

        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('sim/status'))
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        # expect only ResourceB since first agent was removed
        assert_header_monitor_log('date,time,ResourceB', endpoint)


def test_invalid_agent_manager():
    with sim_environment() as endpoint:
        result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('2/list_agents'))
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == 'Invalid agent manager: 2, available agents: [0, 1]'
        assert not result


def test_real_environment_with_misconfigured_agent():
    with contextlib.ExitStack() as stack:
        agent_config = [
            "arps",
            "test_resources",
            "conf",
            "dummy_agent_with_error_in_user_modules.conf",
        ]
        agents_directory_port = stack.enter_context(start_agents_directory())
        agents_directory = {"address": platform.node(), 'port': agents_directory_port}

        config_file = generate_real_env_configuration(
            agent_config, agents_directory, 'raw'
        )
        configuration_file = stack.enter_context(config_file)
        user_defined_parameters = ['--config_file', configuration_file]

        agent_manager_endpoint = stack.enter_context(
            start_agent_manager(user_defined_parameters)
        )
        body, headers = build_http_body_and_header(
            body={'policies': {'DummyPolicy': None}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, agent_manager_endpoint('agents'), body, headers
        )
        assert HTTPStatus.BAD_REQUEST == response.code
        assert (
            "No module named 'arps.test_resources.non_existent_module', "
            "check if module or attribute name exists" == response.reason
        )


def test_real_environment_with_non_existent_agent_file():
    with contextlib.ExitStack() as stack:
        agent_config = ["arps", "test_resources", "conf", "non_existent_file.conf"]
        agents_directory_port = stack.enter_context(start_agents_directory())
        agents_directory = {"address": platform.node(), 'port': agents_directory_port}

        config_file = generate_real_env_configuration(
            agent_config, agents_directory, 'raw'
        )
        configuration_file = stack.enter_context(config_file)
        user_defined_parameters = ['--config_file', configuration_file]

        agent_manager_endpoint = stack.enter_context(
            start_agent_manager(user_defined_parameters)
        )
        body, headers = build_http_body_and_header(
            body={'policies': {'DummyPolicy': None}}
        )
        result, response = invoke_rest_ws(
            HTTPMethods.POST, agent_manager_endpoint('agents'), body, headers
        )
        assert HTTPStatus.BAD_REQUEST == response.code
        assert (
            "agent config file arps/test_resources/conf/non_existent_file.conf doesn't exist"
            == response.reason
        )


@contextlib.contextmanager
def real_environment(comm_layer_type):
    try:
        with contextlib.ExitStack() as stack:
            agent_config = ["arps", "test_resources", "conf", "dummy_agent.conf"]
            agents_directory_port = stack.enter_context(start_agents_directory())
            agents_directory = {
                "address": platform.node(),
                'port': agents_directory_port,
            }

            configuration_file = stack.enter_context(
                generate_real_env_configuration(
                    agent_config, agents_directory, comm_layer_type
                )
            )
            user_defined_parameters = ['--config_file', configuration_file]

            yield stack.enter_context(start_agent_manager(user_defined_parameters))

    except RuntimeError as err:
        print(err)


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
def test_try_to_run_as_simulator_in_real_env(comm_layer_type):
    with real_environment(comm_layer_type) as endpoint:
        expected = 'not running as simulator, check your config files'

        for resource in ('sim/status', 'sim/run', 'sim/stop'):
            content, response = invoke_rest_ws(HTTPMethods.GET, endpoint(resource))
            assert not content
            assert response.code == HTTPStatus.CONFLICT
            assert response.reason == expected


@pytest.fixture(
    params=[
        sim_environment,
        partial(real_environment, 'raw'),
        partial(real_environment, 'REST'),
    ]
)
def endpoint(request):
    """Returns an endpoint builder with a partial url
    (http://agent_manager_host:agent_manager_port)

    """
    try:
        with request.param() as accessor:
            yield accessor
    except (RuntimeError, TimeoutError) as error:
        print(str(error))
        pytest.fail(str(error))


def spawn_agent_dummy_policy(endpoint):
    body, headers = build_http_body_and_header(body={'policies': {'DummyPolicy': None}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert HTTPStatus.OK == response.code
    return result


def test_support_commands(endpoint):
    content, response = invoke_rest_ws(HTTPMethods.GET, endpoint(''))
    assert HTTPStatus.OK == response.code
    general_commands = content['general']
    assert len(general_commands) == 2
    am_commands = content['agent_manager']
    assert len(am_commands) == 9

    content, response = invoke_rest_ws(HTTPMethods.GET, endpoint('about'))
    assert HTTPStatus.OK == response.code
    assert 'version' in content
    assert 'agent_managers' in content
    assert 'simulation' in content

    available_policies, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('policy_repository')
    )
    assert HTTPStatus.OK == response.code
    assert "DummyPolicy" in available_policies
    assert "DummyPeriodicPolicy" in available_policies
    assert "DummyPolicyWithBehavior" in available_policies
    assert "DummyPolicyForSimulator" in available_policies
    assert "DefaultDummyPolicyForSimulator" in available_policies

    # monitor policies are generated to automatically to monitor
    # resources. They are not declared in none of the configuration
    # file
    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('policy_repository'))
    assert HTTPStatus.OK == response.code
    assert 'DummyPolicy' in result
    assert 'DummyPolicyWithBehavior' in result
    assert 'DummyPolicyForSimulator' in result
    assert 'DefaultDummyPolicyForSimulator' in result
    assert 'SenderPolicy' in result
    assert 'ReceiverPolicy' in result
    assert 'ResourceAMonitorPolicy' in result
    assert 'ResourceBMonitorPolicy' in result
    assert 'ResourceCMonitorPolicy' in result
    assert 'ReceivedMessagesResourceMonitorPolicy' in result
    assert 'DummyResourceMonitorPolicy' in result

    available_touchpoints, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('loaded_touchpoints')
    )
    sensors = available_touchpoints['sensors']
    actuators = available_touchpoints['actuators']
    assert 'ResourceA' in sensors
    assert 'ResourceB' in sensors
    assert 'DummyResource' in sensors
    assert 'ResourceB' in actuators
    assert 'ReceivedMessagesResource' in actuators


def list_of_spawned_agents(endpoint):
    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('list_agents'))
    assert response.code == HTTPStatus.OK
    return result['agents']


def test_spawn_agent_fails_no_policy(endpoint):
    body, headers = build_http_body_and_header({'policies': {}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert not result
    assert response.code == HTTPStatus.BAD_REQUEST
    assert response.reason == 'agent not created, no policy specified'

    assert not list_of_spawned_agents(endpoint)


def test_spawn_agent_fails_non_existing_policy(endpoint):
    body, headers = build_http_body_and_header({'policies': {'DummyPolicya': None}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert response.code == HTTPStatus.BAD_REQUEST
    assert response.reason == 'Policy DummyPolicya not registered'

    assert not list_of_spawned_agents(endpoint)


def test_spawn_agent_fails_invalid_period_type_with_regular_policy(endpoint):
    body, headers = build_http_body_and_header({'policies': {'DummyPolicy': 'test'}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason == 'Trying to use period with a non periodic policy DummyPolicy'
    )

    assert not list_of_spawned_agents(endpoint)


def test_spawn_agent_fails_valid_period_type_with_regular_policy(endpoint):
    body, headers = build_http_body_and_header({'policies': {'DummyPolicy': 10}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason == 'Trying to use period with a non periodic policy DummyPolicy'
    )

    assert not list_of_spawned_agents(endpoint)


def test_spawn_agent_fails_invalid_period_type(endpoint):
    body, headers = build_http_body_and_header(
        {'policies': {'DummyPeriodicPolicy': 'test'}}
    )
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason
        == 'Expected positive int period when creating periodic policy DummyPeriodicPolicy'
    )

    assert not list_of_spawned_agents(endpoint)


def test_failed_spawn_agent_with_monitor_policy_when_no_period_is_provided(endpoint):
    body, headers = build_http_body_and_header(
        {'policies': {'ResourceAMonitorPolicy': None}}
    )
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert not result
    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason
        == 'Expected positive int period when creating periodic policy ResourceAMonitorPolicy'
    )


def test_spawn_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    assert list_of_spawned_agents(endpoint) == ['0.1']


def test_spawn_agent_identifier_creation_consistency(endpoint):
    # no ids are created if the process of spawning fails
    assert not list_of_spawned_agents(endpoint)

    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    assert list_of_spawned_agents(endpoint) == ['0.1']

    body, headers = build_http_body_and_header({'policies': {}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert not result
    assert response.code == HTTPStatus.BAD_REQUEST
    assert response.reason == 'agent not created, no policy specified'

    assert list_of_spawned_agents(endpoint) == ['0.1']

    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.2 created'

    assert set(list_of_spawned_agents(endpoint)) == set(['0.1', '0.2'])


def test_single_agent_workflow(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )

    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )
    assert 'related_agents' in response_content
    assert not response_content['related_agents']


def test_invalid_agents_status(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint('agents/0.1'))

    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason == 'expecte request_type parameter(info, sensors, or actuators)'
    )
    assert not result


def test_multiple_agents_workflow(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.2 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=sensors')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['touchpoint'].keys()) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=sensors')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['touchpoint'].keys()) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=actuators')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['touchpoint'].keys()) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=actuators')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['touchpoint'].keys()) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )


def test_multiple_clients_workflow(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(result['content']['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    assert Counter(result['content']['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(result['content']['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )


def test_update_agents_relationship(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.2 created'

    body, headers = build_http_body_and_header({'agent_id': '0.2', 'operation': 'add'})

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/relationship'), body, headers
    )
    assert HTTPStatus.OK == response.code
    assert '0.1' == result['sender_id']
    assert '0.0' == result['receiver_id']
    assert (
        'Operation include_as_related of 0.2 performed in 0.1'
        == result['content']['status']
    )

    body, headers = build_http_body_and_header({'agent_id': '0.1', 'operation': 'add'})

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.2/relationship'), body, headers
    )
    assert HTTPStatus.OK == response.code
    assert '0.2' == result['sender_id']
    assert '0.0' == result['receiver_id']
    assert (
        'Operation include_as_related of 0.1 performed in 0.2'
        == result['content']['status']
    )

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_items = result['content']['related_agents']
    assert ['0.2'] == response_items

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_items = result['content']['related_agents']
    assert ['0.1'] == response_items

    body, headers = build_http_body_and_header(
        {'agent_id': '0.2', 'operation': 'remove'}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/relationship'), body, headers
    )
    assert HTTPStatus.OK == response.code
    assert result

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_items = result['content']['related_agents']
    assert not response_items

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_items = result['content']['related_agents']
    assert ['0.1'] == response_items


def test_add_self_relationship(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    body, headers = build_http_body_and_header({'agent_id': '0.1', 'operation': 'add'})
    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/relationship'), body, headers
    )
    assert HTTPStatus.BAD_REQUEST == response.code
    assert 'Operation with itself not permitted' == response.reason


def test_remove_inexistent_relationship(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.2 created'

    body, headers = build_http_body_and_header(
        {'agent_id': '0.2', 'operation': 'remove'}
    )
    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/relationship'), body, headers
    )
    assert HTTPStatus.BAD_REQUEST == response.code
    assert 'Agent 0.1 has no relationship with agent 0.2' == response.reason


def test_add_policy_to_running_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )

    body, headers = build_http_body_and_header(
        {'operation': 'add', 'policy': 'DummyPeriodicPolicy', 'period': 1}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/policy'), body, headers
    )
    assert HTTPStatus.OK == response.code
    assert '0.1' == result['sender_id']
    assert '0.0' == result['receiver_id']

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
            'DummyPeriodicPolicy',
        ]
    )


def test_error_add_policy_to_running_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )

    body, headers = build_http_body_and_header(
        {'operation': 'add', 'policy': 'DummyPeriodicPolicya', 'period': 1}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/policy'), body, headers
    )
    assert HTTPStatus.BAD_REQUEST == response.code
    assert 'policy DummyPeriodicPolicya not registered' == response.reason
    assert not result

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )


def test_error_add_periodic_policy_to_running_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )

    body, headers = build_http_body_and_header(
        {'operation': 'add', 'policy': 'DummyPeriodicPolicy'}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/policy'), body, headers
    )
    assert HTTPStatus.BAD_REQUEST == response.code
    assert (
        'Expected positive int period when creating periodic policy DummyPeriodicPolicy'
        == response.reason
    )
    assert not result

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )


def test_remove_policy_from_running_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )

    body, headers = build_http_body_and_header(
        {'operation': 'remove', 'policy': 'DummyPolicy'}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/policy'), body, headers
    )
    assert HTTPStatus.OK == response.code
    assert '0.1' == result['sender_id']
    assert '0.0' == result['receiver_id']

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
        ]
    )


def test_remove_non_existing_policy(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )

    body, headers = build_http_body_and_header(
        {'operation': 'remove', 'policy': 'DummyPeriodicPolicya'}
    )

    result, response = invoke_rest_ws(
        HTTPMethods.PUT, endpoint('agents/0.1/policy'), body, headers
    )
    assert HTTPStatus.BAD_REQUEST == response.code
    assert 'policy DummyPeriodicPolicya not registered' == response.reason
    assert not result

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )
    assert HTTPStatus.OK == response.code
    response_content = result['content']

    assert Counter(response_content['sensors']) == Counter(
        ['ResourceA', 'ResourceB', 'DummyResource']
    )
    assert Counter(response_content['actuators']) == Counter(
        ['ResourceB', 'ResourceC', 'ReceivedMessagesResource']
    )
    assert Counter(response_content['policies']) == Counter(
        [
            'InfoProviderPolicy',
            'TouchPointStatusProviderPolicy',
            'MetaPolicyProvider',
            'MetaAgentProviderPolicy',
            'DummyPolicy',
        ]
    )


def test_invalid_id_on_terminate_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    assert list_of_spawned_agents(endpoint) == ['0.1']

    result, response = invoke_rest_ws(HTTPMethods.DELETE, endpoint('agents/0.2'))
    assert not result
    assert response.code == HTTPStatus.BAD_REQUEST
    assert (
        response.reason
        == 'Agent id not found. Try list_agents resource to list available agents'
    )


def test_terminate_agent(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.2 created'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )

    assert HTTPStatus.OK == response.code

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=info')
    )

    assert HTTPStatus.OK == response.code

    assert ['0.1', '0.2'] == list_of_spawned_agents(endpoint)

    result, response = invoke_rest_ws(HTTPMethods.DELETE, endpoint('agents/0.1'))

    possible_message_one = 'Agent 0.1 terminated successfully'
    possible_message_two = (
        'Return code is not 0, agent 0.1 has been forcefully terminated'
    )
    assert result in [
        possible_message_one,
        possible_message_two,
    ], f'unexpected result: {result}'

    assert ['0.2'] == list_of_spawned_agents(endpoint)

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.1?request_type=info')
    )

    assert response.code == HTTPStatus.NOT_FOUND
    assert response.reason == 'Resource /0.1 not found; Agent ID 0.1 is not running'

    result, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('agents/0.2?request_type=info')
    )

    assert HTTPStatus.OK == response.code


def test_missing_agent_id(endpoint):

    for http_methods in (HTTPMethods.GET, HTTPMethods.PUT, HTTPMethods.DELETE):
        result, response = invoke_rest_ws(http_methods, endpoint('agents'))
        assert not result
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == "Missing agent id: '/agents/{agent_id}'"


def assert_failure_monitor_log_request(endpoint):
    content, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('monitor_logs'), json_resource=False
    )

    assert HTTPStatus.BAD_REQUEST == response.code
    assert 'No monitoring agent was spawned' == response.reason


def assert_header_monitor_log(expected_header, endpoint):
    content, response = invoke_rest_ws(
        HTTPMethods.GET, endpoint('monitor_logs'), json_resource=False
    )

    assert HTTPStatus.OK == response.code
    with io.StringIO(content.decode()) as monitor_log_fh:
        header = monitor_log_fh.readline().strip()
        assert (
            header == expected_header
        ), f'Expected header "{expected_header}", got "{header}"'


def spawn_monitor_policy(endpoint, monitor_policy, period):
    body, headers = build_http_body_and_header({'policies': {monitor_policy: period}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, endpoint('agents'), body, headers
    )
    assert HTTPStatus.OK == response.code
    return result


def test_spawn_agent_with_monitor_policy(endpoint):
    assert (
        spawn_monitor_policy(endpoint, 'ResourceAMonitorPolicy', 1)
        == 'Agent 0.1 created'
    )

    assert_header_monitor_log('date,time,ResourceA', endpoint)


def test_spawn_two_agents_with_same_monitor_policy(endpoint):
    assert (
        spawn_monitor_policy(endpoint, 'ResourceAMonitorPolicy', 1)
        == 'Agent 0.1 created'
    )

    assert_header_monitor_log('date,time,ResourceA', endpoint)

    assert (
        spawn_monitor_policy(endpoint, 'ResourceAMonitorPolicy', 3)
        == 'Agent 0.2 created'
    )

    assert_header_monitor_log('date,time,ResourceA_x,ResourceA_y', endpoint)


def test_spawn_two_agents_with_different_monitor_policy(endpoint):
    assert (
        spawn_monitor_policy(endpoint, 'ResourceAMonitorPolicy', 1)
        == 'Agent 0.1 created'
    )

    assert_header_monitor_log('date,time,ResourceA', endpoint)

    assert (
        spawn_monitor_policy(endpoint, 'ResourceBMonitorPolicy', 1)
        == 'Agent 0.2 created'
    )

    assert_header_monitor_log('date,time,ResourceA,ResourceB', endpoint)


def test_regular_agent_together_with_agent_monitor(endpoint):
    assert spawn_agent_dummy_policy(endpoint) == 'Agent 0.1 created'

    assert (
        spawn_monitor_policy(endpoint, 'ResourceAMonitorPolicy', 1)
        == 'Agent 0.2 created'
    )

    assert_header_monitor_log('date,time,ResourceA', endpoint)


if __name__ == '__main__':
    pytest.main([__file__])
