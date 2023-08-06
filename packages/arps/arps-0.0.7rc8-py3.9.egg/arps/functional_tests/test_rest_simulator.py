'''This modules try to cover all features present in the simulator

Expected events is a list of tuples. Each tuple represent the
event's identifier, arrival_time, start_time, and finished_time

'''

import json
import pathlib
from http import HTTPStatus
from time import sleep

import pytest  # type: ignore

from arps.core.real.rest_api_utils import (
    HTTPMethods,
    build_http_body_and_header,
    invoke_rest_ws,
)
from arps.core.simulator.resource import EvtType
from arps.test_resources.rest_simulator_helper import (
    retrieve_last_result,
    setup_access_resource,
    verify_simulation_results,
)

# pylint:disable=redefined-outer-name

MAS = EvtType.mas.name
DES_PRE = EvtType.des_pre.name
DES_POS = EvtType.des_pos.name
INDIRECT = EvtType.rsc_indirect.name
NONE = EvtType.none.name


@pytest.fixture
def sim_access_resource():
    sim_configuration_path = (
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment.conf'
    )
    with setup_access_resource(sim_configuration_path, debug=True) as partial_uri:
        yield partial_uri


def test_sim_index(sim_access_resource):
    content, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim'))
    assert response.code == HTTPStatus.OK
    available_commands = content['available_commands']
    assert len(available_commands.keys()) == 6
    assert 'run' in available_commands
    assert 'stop' in available_commands
    assert 'status' in available_commands
    assert 'result' in available_commands
    assert 'save' in available_commands
    assert 'stats' in available_commands


def test_stop_simulator(sim_access_resource):
    result, response = invoke_rest_ws(
        HTTPMethods.GET, sim_access_resource('sim/status')
    )
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/run'))
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/stop'))
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'


def test_simulator_stats_error(sim_access_resource):
    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/stats'))
    assert response.code == HTTPStatus.CONFLICT
    assert response.reason == 'No simulation has been executed so far'
    assert result == {}


def test_run_simulator_baseline(sim_access_resource):
    """
    Run simulator with no agents
    """
    result, response = invoke_rest_ws(
        HTTPMethods.GET, sim_access_resource('sim/status')
    )
    assert result == 'stopped'
    assert response.code == HTTPStatus.OK

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/run'))
    assert result == 'running'
    assert response.code == HTTPStatus.OK

    result, response = invoke_rest_ws(
        HTTPMethods.GET, sim_access_resource('sim/status')
    )
    while result == 'running':
        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/status')
        )
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    result, response = invoke_rest_ws(
        HTTPMethods.GET, sim_access_resource('sim/status')
    )
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    expected_result = [
        ('0', 'ResourceA', '1', '50', '1', DES_PRE),
        ('1', 'ResourceB', '1', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '1', '70', '2', DES_PRE),
        ('1', 'ResourceB', '1', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '1', '50', '2', DES_POS),
        ('1', 'ResourceB', '1', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '2', '80', '3', DES_PRE),
        ('1', 'ResourceB', '2', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '3', '100', '4', DES_PRE),
        ('0', 'ResourceA', '3', '90', '1', DES_POS),
        ('0', 'ResourceA', '3', '70', '4', DES_POS),
        ('0', 'ResourceA', '4', '40', '3', DES_POS),
        ('1', 'ResourceB', '4', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '5', '70', '5', DES_PRE),
        ('1', 'ResourceB', '5', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '5', '40', '5', DES_POS),
        ('1', 'ResourceB', '5', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '7', '50', '6', DES_PRE),
        ('0', 'ResourceA', '8', '40', '6', DES_POS),
    ]

    _, sim_last_result, events = retrieve_last_result(sim_access_resource)
    verify_simulation_results(initial_log_events() + expected_result, sim_last_result)
    expected_events = [
        ('2', '0', '1', '1', '1', 'initial state: 20'),
        ('1', '0', '1', '1', '3', 'initial state: 10'),
        ('4', '0', '3', '3', '3', 'initial state: 20'),
        ('3', '0', '2', '2', '4', 'initial state: 30'),
        ('5', '0', '5', '5', '5', 'initial state: 30'),
        ('6', '0', '7', '7', '8', 'initial state: 10'),
    ]
    assert expected_events == events

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/stats'))
    assert response.code == HTTPStatus.OK
    assert 'elapsed_time' in result
    assert 'tracemalloc' in result and len(result['tracemalloc']) == 10
    assert 'total_memory' in result


def test_run_simulator_with_one_agent(sim_access_resource):
    """
    Run simulator with one agent
    """
    body, headers = build_http_body_and_header(
        {
            'policies': {
                'DefaultDummyPolicyForSimulator': 1,
                'DummyPolicyForSimulator': 1,
            }
        }
    )
    url = sim_access_resource('agents')
    result, response = invoke_rest_ws(HTTPMethods.POST, url, body, headers)
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.1 created'

    status_endpoint = sim_access_resource('sim/status')
    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    url = sim_access_resource('sim/run')
    result, response = invoke_rest_ws(HTTPMethods.GET, url)
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    while result == 'running':
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    # ResourceA is modified by the tasks. ResourceC is modified by
    # the agent. It reads ResourceB. If value of ResourceB is greater
    # than 11, than it decrements ResourceC, otherwise it increments
    # ResourceC

    # ResourceB is modified indirectly by the control of ResourceA. If
    # ResourceA is above 30, ResourceB is set to ON, otherwise it is
    # set to OFF

    # When there is no more modification of ResourceB, its value is
    # 25. This makes the agent increment the ResourceC indefinetely

    expected_result = [
        ('0', 'ResourceA', '1', '50', '1', DES_PRE),
        ('1', 'ResourceB', '1', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '1', '70', '2', DES_PRE),
        ('1', 'ResourceB', '1', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '1', '50', '2', DES_POS),
        ('1', 'ResourceB', '1', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceC', '1', '39', '0.1', MAS),
        ('0', 'ResourceA', '2', '80', '3', DES_PRE),
        ('1', 'ResourceB', '2', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceC', '2', '38', '0.1', MAS),
        ('0', 'ResourceA', '3', '100', '4', DES_PRE),
        ('0', 'ResourceA', '3', '90', '1', DES_POS),
        ('0', 'ResourceA', '3', '70', '4', DES_POS),
        ('0', 'ResourceC', '3', '37', '0.1', MAS),
        ('0', 'ResourceA', '4', '40', '3', DES_POS),
        ('1', 'ResourceB', '4', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceC', '4', '36', '0.1', MAS),
        ('0', 'ResourceA', '5', '70', '5', DES_PRE),
        ('1', 'ResourceB', '5', 'ON', 'ResourceA', INDIRECT),
        ('0', 'ResourceA', '5', '40', '5', DES_POS),
        ('1', 'ResourceB', '5', 'OFF', 'ResourceA', INDIRECT),
        ('0', 'ResourceC', '5', '35', '0.1', MAS),
        ('0', 'ResourceC', '6', '34', '0.1', MAS),
        ('0', 'ResourceA', '7', '50', '6', DES_PRE),
        ('0', 'ResourceC', '7', '33', '0.1', MAS),
        ('0', 'ResourceA', '8', '40', '6', DES_POS),
        ('0', 'ResourceC', '8', '32', '0.1', MAS),
        ('0', 'ResourceC', '9', '31', '0.1', MAS),
    ]

    _, sim_last_result, events = retrieve_last_result(sim_access_resource)
    expected = initial_log_events() + expected_result
    index = sim_last_result.index(('0', 'ResourceC', '10', '30', '0.1', MAS))
    last_result = sim_last_result[:index]
    remainder = sim_last_result[index:]
    verify_simulation_results(expected, last_result)

    for i in remainder:
        assert ('0', 'ResourceC', '0.1', MAS) == (i[0], i[1], i[4], i[5])

    expected_events = [
        ('2', '0', '1', '1', '1', 'initial state: 20'),
        ('1', '0', '1', '1', '3', 'initial state: 10'),
        ('4', '0', '3', '3', '3', 'initial state: 20'),
        ('3', '0', '2', '2', '4', 'initial state: 30'),
        ('5', '0', '5', '5', '5', 'initial state: 30'),
        ('6', '0', '7', '7', '8', 'initial state: 10'),
    ]
    assert expected_events == events


def test_run_simulator_with_multiple_agent(sim_access_resource):
    """
    Run simulator with one agent
    """
    body, headers = build_http_body_and_header(
        {
            'policies': {
                'DefaultDummyPolicyForSimulator': 1,
                'DummyPolicyForSimulator': 1,
            }
        }
    )
    url = sim_access_resource('agents')
    result, response = invoke_rest_ws(HTTPMethods.POST, url, body, headers)
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.1 created'

    url = sim_access_resource('agents')
    result, response = invoke_rest_ws(HTTPMethods.POST, url, body, headers)
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.2 created'

    url = sim_access_resource('agents')
    result, response = invoke_rest_ws(HTTPMethods.POST, url, body, headers)
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.3 created'

    status_endpoint = sim_access_resource('sim/status')
    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    url = sim_access_resource('sim/run')
    result, response = invoke_rest_ws(HTTPMethods.GET, url)
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    while result == 'running':
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    _, sim_last_result, events = retrieve_last_result(sim_access_resource)
    mas_events = [i[4] for i in sim_last_result if i[5] == MAS]
    mas_events_deterministic = ['0.1', '0.2', '0.3'] * 19
    assert not mas_events_deterministic == mas_events
    other_events = [i[4] for i in sim_last_result if i[5] != MAS]
    other_events = other_events[8:]
    other_events_deterministic = [
        '1',
        'ResourceA',
        '2',
        'ResourceA',
        '2',
        'ResourceA',
        '3',
        'ResourceA',
        '4',
        '1',
        '4',
        '3',
        'ResourceA',
        '5',
        'ResourceA',
        '5',
        'ResourceA',
        '6',
        '6',
    ]
    assert other_events == other_events_deterministic

    expected_events = [
        ('2', '0', '1', '1', '1', 'initial state: 20'),
        ('1', '0', '1', '1', '3', 'initial state: 10'),
        ('4', '0', '3', '3', '3', 'initial state: 20'),
        ('3', '0', '2', '2', '4', 'initial state: 30'),
        ('5', '0', '5', '5', '5', 'initial state: 30'),
        ('6', '0', '7', '7', '8', 'initial state: 10'),
    ]
    assert expected_events == events


def test_last_sim_result(sim_access_resource):
    status_endpoint = sim_access_resource('sim/status')
    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/run'))
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    while result == 'running':
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    result, response = invoke_rest_ws(
        HTTPMethods.GET, sim_access_resource('sim/status')
    )
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    metadata, result, events = retrieve_last_result(sim_access_resource)
    assert len(result) == 27
    assert len(events) == 6

    metadata_content = json.loads(metadata)
    assert 'ResourceA' in metadata_content.keys()
    assert 'ResourceB' in metadata_content.keys()
    assert 'ResourceC' in metadata_content.keys()
    assert 'ReceivedMessagesResource' in metadata_content.keys()


def test_last_result_fail(sim_access_resource):
    endpoint = sim_access_resource('sim/result')
    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint)
    assert (
        response.reason
        == 'Error while retrieving last result file. Did you run the simulation? Did you stop the running simulation?'
    )
    assert response.code == HTTPStatus.CONFLICT
    assert not result


def test_save_simulation_configuration(sim_access_resource):
    spawn_agent_endpoint = sim_access_resource('agents')
    body, headers = build_http_body_and_header(
        {
            'policies': {
                'DefaultDummyPolicyForSimulator': 1,
                'DummyPolicyForSimulator': 1,
            }
        }
    )
    result, response = invoke_rest_ws(
        HTTPMethods.POST, spawn_agent_endpoint, body, headers
    )
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.1 created'

    body, headers = build_http_body_and_header({'policies': {'DummyPolicy': None}})
    result, response = invoke_rest_ws(
        HTTPMethods.POST, spawn_agent_endpoint, body, headers
    )
    assert response.code == HTTPStatus.OK
    assert result == 'Agent 0.2 created'

    status_endpoint = sim_access_resource('sim/status')
    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    endpoint = sim_access_resource('sim/run')
    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    while result == 'running':
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    endpoint = sim_access_resource('sim/save')
    result, response = invoke_rest_ws(HTTPMethods.GET, endpoint)
    assert response.code == HTTPStatus.OK

    assert result == {
        '0': [
            {
                'command': 'spawn_agent',
                'params': {
                    'policies': {
                        'DefaultDummyPolicyForSimulator': '1',
                        'DummyPolicyForSimulator': '1',
                    }
                },
            },
            {'command': 'spawn_agent', 'params': {'policies': {'DummyPolicy': 'None'}}},
        ],
        '1': [],
    }

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/stop'))
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'


def test_finite_stochastic_simulation():
    sim_configuration_path = (
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment_random_events.conf'
    )
    with setup_access_resource(sim_configuration_path) as sim_access_resource:
        status_endpoint = sim_access_resource('sim/status')
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/run')
        )
        assert response.code == HTTPStatus.OK
        assert result == 'running'

        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        while result == 'running':
            result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
            assert response.code == HTTPStatus.OK
            sleep(0.15)

        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/status')
        )
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        # TODO: use random.seed to control this
        _, result, events = retrieve_last_result(sim_access_resource)
        # since there are 40 events generated, as specified in the
        # dummy_simulator_environment_random_events.conf, it is
        # excepted that more than 80 results will be present due to
        # the tasks main and pos method. Also, indirect modifications
        # are expected.
        assert len(result) > 80
        assert len(events) == 40


def test_infinite_stochastic_simulation():
    sim_configuration_path = (
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment_random_infinite_events.conf'
    )
    with setup_access_resource(sim_configuration_path) as sim_access_resource:
        status_endpoint = sim_access_resource('sim/status')
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/run')
        )
        assert response.code == HTTPStatus.OK
        assert result == 'running'

        # I could wait for as long as I wanted. The test above runs the
        # simulation in less than 0.05 seconds.
        sleep(1)  # half second is enough

        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/stop')
        )
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        result, response = invoke_rest_ws(
            HTTPMethods.GET, sim_access_resource('sim/status')
        )
        assert response.code == HTTPStatus.OK
        assert result == 'stopped'

        # TODO: use random.seed to control this
        _, result, events = retrieve_last_result(sim_access_resource)
        # since there are 40 events generated, as specified in the
        # dummy_simulator_environment_random_events.conf, it is
        # excepted that more than 80 results will be present due to
        # the tasks main and pos method. Also, indirect modifications
        # are expected.
        assert len(result) > 400
        assert len(events) > 400  # we can see that there are way more events


def initial_log_events():
    return [
        ('0', 'DummyResource', '0', 'FakeResource', 'None', NONE),
        ('0', 'ReceivedMessagesResource', '0', '0', 'None', NONE),
        ('0', 'ResourceA', '0', '40', 'None', NONE),
        ('0', 'ResourceB', '0', 'ON', 'None', NONE),
        ('0', 'ResourceC', '0', '40', 'None', NONE),
        ('1', 'ReceivedMessagesResource', '0', '0', 'None', NONE),
        ('1', 'ResourceA', '0', '37', 'None', NONE),
        ('1', 'ResourceB', '0', 'ON', 'None', NONE),
    ]


if __name__ == '__main__':
    pytest.main([__file__])
