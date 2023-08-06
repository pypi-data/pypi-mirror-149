import contextlib
import copy
import itertools
import json
import operator
import pathlib
import tempfile

import pytest  # type: ignore

from arps.apps.configuration_file_loader import (
    InvalidConfigurationError,
    load_agent_environment,
    load_attribute,
    load_event_queue_loader,
    load_manager_environment,
    load_resources_table,
)
from arps.core.mobile_entity import Coordinates
from arps.core.resources_table import ResourcesTable
from arps.test_resources.configuration_template import generate_real_env_configuration


def test_load_resources_table():
    resources_module = 'arps.test_resources.dummies'
    resources_table = ResourcesTable(environment_types={1: 0, 2: 0})
    agent_resources_1 = [
        {'class': 'ResourceA', 'initial_state': 32},
        {'class': 'ResourceB', 'initial_state': 'ON', 'attributes': {'a': 20}},
        {'class': 'ResourceC', 'initial_state': 80},
    ]

    agent_resources_2 = [
        {'class': 'ResourceA', 'initial_state': 100},
        {'class': 'ResourceB', 'initial_state': 'ON'},
        {'class': 'ResourceC', 'attributes': {'test': 10}},
        {'class': 'ReceivedMessagesResource'},
    ]

    load_resources_table(1, resources_table, resources_module, agent_resources_1)
    load_resources_table(2, resources_table, resources_module, agent_resources_2)

    resources_in_environment = resources_table.resources_from_environment(
        environment_id=1
    )

    resource = resources_in_environment['ResourceA']
    assert resource.value == 32
    resource = resources_in_environment['ResourceB']
    assert resource.value == 'ON'
    assert resource.a == 20
    resource = resources_in_environment['ResourceC']
    assert resource.value == 80

    resources_in_environment = resources_table.resources_from_environment(
        environment_id=2
    )

    resource = resources_in_environment['ResourceA']
    assert resource.value == 100
    resource = resources_in_environment['ResourceB']
    assert resource.value == 'ON'
    resource = resources_in_environment['ResourceC']
    assert resource.value is None
    assert resource.test == 10
    resource = resources_in_environment['ReceivedMessagesResource']
    assert resource.value == 0


AGENT_CONF_TEMPLATE = {
    "user_defined_base_module": "arps.test_resources.dummies",
    "resources": [
        {"class": "ResourceA", "initial_state": 40, "affects": {"1": ["ResourceB"]}},
        {"class": "ResourceB", "initial_state": "ON"},
        {"class": "ResourceC", "initial_state": 40},
        {"class": "ReceivedMessagesResource"},
        {"class": "DummyResource"},
    ],
    "agent_config": {
        "sensors": [
            {"resource_id": "ResourceA", "class": "Sensor"},
            {"resource_id": "ResourceB", "class": "Sensor"},
            {"resource_id": "DummyResource", "class": "Sensor"},
        ],
        "actuators": [
            {"resource_id": "ResourceB", "class": "Actuator"},
            {"resource_id": "ResourceC", "class": "Actuator"},
            {"resource_id": "ReceivedMessagesResource", "class": "Actuator"},
        ],
        "policies": [
            "DummyPolicy",
            "DummyPeriodicPolicy",
            "DummyPolicyWithBehavior",
            "DummyPolicyForSimulator",
            "DefaultDummyPolicyForSimulator",
            "SenderPolicy",
            "ReceiverPolicy",
        ],
    },
}


def test_load_agent():
    with tempfile.TemporaryDirectory(prefix='_agent_conf_dir') as temp_dir:
        filename = pathlib.Path(temp_dir) / 'agent.conf'
        with open(filename, 'w') as fh:
            json.dump(AGENT_CONF_TEMPLATE, fh)

        environment = load_agent_environment(1, filename)

        assert environment.is_policy_registered('DummyPolicy')
        assert environment.boundaries is None

        sensor_ids = environment.sensors.keys()
        assert 'ResourceA' in sensor_ids
        assert 'ResourceB' in sensor_ids

        sensor = environment.sensors['ResourceA']
        assert sensor.resource.value == 40
        sensor = environment.sensors['ResourceB']
        assert sensor.resource.value == 'ON'

        actuator_ids = environment.actuators.keys()
        assert 'ResourceB' in actuator_ids
        assert 'ResourceC' in actuator_ids
        assert 'ReceivedMessagesResource' in actuator_ids

        actuator = environment.actuators['ResourceB']
        assert actuator.resource.value == 'ON'

        actuator = environment.actuators['ReceivedMessagesResource']
        assert actuator.resource.value == 0

        actuator = environment.actuators['ResourceC']
        assert actuator.resource.value == 40

        assert environment.is_policy_registered('ResourceAMonitorPolicy')
        assert environment.is_policy_registered('ResourceBMonitorPolicy')
        assert environment.is_policy_registered('ResourceCMonitorPolicy')
        assert environment.is_policy_registered('ReceivedMessagesResourceMonitorPolicy')


def test_load_spatial_agent():
    SPATIAL_AGENT_CONF = copy.deepcopy(AGENT_CONF_TEMPLATE)
    SPATIAL_AGENT_CONF['boundaries'] = {
        'upper_bound': [1, 1, 1],
        'lower_bound': [0, 0, 0],
    }
    with tempfile.TemporaryDirectory(prefix='_agent_conf_dir') as temp_dir:
        filename = pathlib.Path(temp_dir) / 'agent.conf'
        with open(filename, 'w') as fh:
            json.dump(SPATIAL_AGENT_CONF, fh)

        environment = load_agent_environment(1, filename)
        assert environment.boundaries.lower == Coordinates(0, 0, 0)
        assert environment.boundaries.upper == Coordinates(1, 1, 1)


def test_load_sim_environment():
    sim_environment_conf = (
        pathlib.Path('arps')
        / 'test_resources'
        / 'conf'
        / 'dummy_simulator_environment.conf'
    )
    manager_environment = load_manager_environment(sim_environment_conf)
    assert manager_environment.pmt is None

    assert manager_environment.run_as_simulator
    environment_manager_zero = (
        manager_environment.resources_table.resources_from_environment(environment_id=0)
    )

    resource_a = environment_manager_zero['ResourceA']
    assert resource_a
    assert environment_manager_zero['ResourceB']
    assert environment_manager_zero['ResourceC']
    assert environment_manager_zero['ReceivedMessagesResource']
    with pytest.raises(IndexError):
        assert environment_manager_zero['InvalidResourceClass']

    environment_manager_one = (
        manager_environment.resources_table.resources_from_environment(environment_id=1)
    )
    assert environment_manager_one['ResourceA']
    resource_b = environment_manager_one['ResourceB']
    assert resource_b
    assert environment_manager_one['ReceivedMessagesResource']
    with pytest.raises(IndexError):
        assert environment_manager_one['ResourceC']

    assert resource_a._affected_resource == resource_b

    manager = manager_environment.configuration[0]
    assert 0 == manager.identifier

    environment = manager.agent_environment
    assert environment.is_policy_registered('DummyPolicy')

    sensor_ids = environment.sensors.keys()
    assert 'ResourceA' in sensor_ids
    assert 'ResourceB' in sensor_ids

    sensor = environment.sensors['ResourceA']
    assert sensor.resource.value == 40
    sensor = environment.sensors['ResourceB']
    assert sensor.resource.value == 'ON'

    actuator_ids = environment.actuators.keys()
    assert 'ResourceB' in actuator_ids
    assert 'ResourceC' in actuator_ids

    actuator = environment.actuators['ResourceB']
    assert actuator.resource.value == 'ON'

    actuator = environment.actuators['ResourceC']
    assert actuator.resource.value == 40

    assert manager_environment.results_path == pathlib.Path(*['logs'])


SIM_CONF_TEMPLATE = {
    "run_as_simulator": True,
    "user_defined_base_module": "arps.test_resources.dummies",
    "environments": [
        {
            "identifier": None,
            "type": 0,
            "resources": [{"class": "ResourceA", "initial_state": 40}],
            "agent_config": {
                "sensors": [
                    {"resource_id": "ResourceA", "class": "Sensor"},
                ],
                "actuators": [],
                "policies": [],
            },
        }
    ],
    "simulator": {
        "event_queue": {
            "deterministic": True,
            "generator": {
                "file": ["arps", "test_resources", "dummies", "dummy_jobs.txt"],
                "factory": {
                    "module": "arps.test_resources.dummies.dummy_event_factory",
                    "class": "DummyEventFactory",
                },
            },
            "resources_estimator": [
                {
                    "environment": 0,
                    "estimators": [
                        {
                            "name": "main_estimate",
                            "module": "arps.test_resources.dummies.dummy_estimators",
                            "estimator": "dummy_main_estimator",
                        },
                        {
                            "name": "pos_estimate",
                            "module": "arps.test_resources.dummies.dummy_estimators",
                            "estimator": "dummy_pos_estimator",
                        },
                    ],
                }
            ],
        },
        "scheduler": {
            "module": "arps.core.simulator.sim_event_scheduler",
            "class": "SimEventScheduler",
        },
        "results_path": ["logs"],
        "log_formatter": {
            "module": "arps.test_resources.dummies.dummy_resource",
            "class": "DummyCategory",
        },
    },
}


@contextlib.contextmanager
def custom_environment(configuration):
    """Create a configuration file based on configuration parameter

    Yields the manager environment
    """
    with tempfile.TemporaryDirectory(suffix='sim_homogeneous_env_conf') as td:
        sim_environment_conf = (
            pathlib.Path(td) / 'dummy_simulator_homogeneous_environment.conf'
        )
        with open(sim_environment_conf, 'w') as tmp_fh:
            json.dump(configuration, tmp_fh)

        manager_environment = load_manager_environment(sim_environment_conf)
        assert manager_environment.pmt is None

        assert manager_environment.run_as_simulator

        yield manager_environment


def test_load_sim_homogenous_environment():
    """This test evalutes environment creation when 'identifier' using
    START..END format, where START and END are integers and START is
    less or equal END

    """
    homogeneous_valid_conf = copy.deepcopy(SIM_CONF_TEMPLATE)
    start = 0
    end = 10
    homogeneous_valid_conf['environments'][0]['identifier'] = f'{start}..{end}'

    with custom_environment(homogeneous_valid_conf) as environment:
        for i in range(start, end + 1):
            environment_manager = (
                environment.resources_table.resources_from_environment(environment_id=i)
            )
            assert environment_manager['ResourceA']


def test_load_sim_homogenous_environment_invalid():
    """This test evalutes environment creation when 'identifier' using
    START..END format, where START and END are integers and START is
    less or equal END

    """
    homogeneous_valid_conf = copy.deepcopy(SIM_CONF_TEMPLATE)
    start = 20
    end = 10
    homogeneous_valid_conf['environments'][0]['identifier'] = f'{start}..{end}'
    with pytest.raises(InvalidConfigurationError) as exception:
        with custom_environment(homogeneous_valid_conf):
            pass

        message = 'Error while creating homogeneous environment. Reason: {reason}'
        assert str(exception.value) == message.format(
            reason='start id must be greater or equal than 0 and start id must be less than end id'
        )


def test_load_bounded_environment():
    """This test evaluates environment where agents have spatial location

    It is using the sim_conf_template, but it is intended to be used
    in both actual and simulated environments

    """
    bounded_valid_conf = copy.deepcopy(SIM_CONF_TEMPLATE)
    bounded_valid_conf['environments'][0]['identifier'] = 0
    bounded_valid_conf['environments'][0]['boundaries'] = {
        'lower_bound': [0, 0, 0],
        'upper_bound': [1, 1, 1],
    }

    with custom_environment(bounded_valid_conf) as manager_environment:
        environment = manager_environment.configuration[0].agent_environment
        assert environment.boundaries.upper == Coordinates(1, 1, 1)
        assert environment.boundaries.lower == Coordinates(0, 0, 0)


def test_load_deterministc_event_queue_loader():
    simulator_properties = {
        'event_queue': {
            'deterministic': True,
            'generator': {
                'file': ['arps', 'test_resources', 'dummies', 'dummy_jobs.txt'],
                'factory': {
                    'module': 'arps.test_resources.dummies.dummy_event_factory',
                    'class': 'DummyEventFactory',
                },
            },
            'resources_estimator': [
                {
                    'environment': 0,
                    'estimators': [
                        {
                            'name': 'main_estimate',
                            'module': 'arps.test_resources.dummies.dummy_estimators',
                            'estimator': 'dummy_main_estimator',
                        },
                        {
                            'name': 'pos_estimate',
                            'module': 'arps.test_resources.dummies.dummy_estimators',
                            'estimator': 'dummy_pos_estimator',
                        },
                    ],
                }
            ],
        }
    }
    resources_table = ResourcesTable({})
    event_queue_loader = load_event_queue_loader(
        simulator_properties['event_queue'], resources_table
    )

    event_queue = iter(event_queue_loader)

    arrivals_time = [1, 1, 2, 3, 5, 7]
    for arrival_time, event in zip(arrivals_time, event_queue):
        assert arrival_time == event.arrival_time


def test_load_stochastic_finite_event_queue_loader():
    simulator_properties = {
        'event_queue': {
            'deterministic': False,
            'generator': {
                'number_of_random_events': 10,
                'random': {
                    'module': 'arps.test_resources.dummies.dummy_event_factory',
                    'class': 'DummyEventParamsGenerator',
                },
                'factory': {
                    'module': 'arps.test_resources.dummies.dummy_event_factory',
                    'class': 'DummyEventFactory',
                },
            },
        },
        'resources_estimator': [
            {
                'environment': 0,
                'estimators': [
                    {
                        'name': 'main_estimate',
                        'module': 'arps.test_resources.dummies.dummy_estimators',
                        'estimator': 'dummy_main_estimator',
                    },
                    {
                        'name': 'pos_estimate',
                        'module': 'arps.test_resources.dummies.dummy_estimators',
                        'estimator': 'dummy_pos_estimator',
                    },
                ],
            }
        ],
    }

    resources_table = ResourcesTable({})
    event_queue_loader = load_event_queue_loader(
        simulator_properties['event_queue'], resources_table
    )

    event_queue = iter(event_queue_loader)
    events = list(event_queue)
    assert len(events) == 10
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events


def test_load_stochastic_infinite_event_queue_loader():
    simulator_properties = {
        'event_queue': {
            'deterministic': False,
            'generator': {
                'random': {
                    'module': 'arps.test_resources.dummies.dummy_event_factory',
                    'class': 'DummyEventParamsGenerator',
                },
                'factory': {
                    'module': 'arps.test_resources.dummies.dummy_event_factory',
                    'class': 'DummyEventFactory',
                },
            },
        },
        'resources_estimator': [
            {
                'environment': 0,
                'estimators': [
                    {
                        'name': 'main_estimate',
                        'module': 'arps.test_resources.dummies.dummy_estimators',
                        'estimator': 'dummy_main_estimator',
                    },
                    {
                        'name': 'pos_estimate',
                        'module': 'arps.test_resources.dummies.dummy_estimators',
                        'estimator': 'dummy_pos_estimator',
                    },
                ],
            }
        ],
    }

    resources_table = ResourcesTable({})
    event_queue_loader = load_event_queue_loader(
        simulator_properties['event_queue'], resources_table
    )

    events = list(itertools.islice(event_queue_loader, 0, 100))
    assert len(events) == 100
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events

    events = list(itertools.islice(event_queue_loader, 0, 10000))
    assert len(events) == 10000
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events


@pytest.mark.parametrize(
    'conf_file_name,comm_layer_type',
    [
        ('dummy_real_environment.conf', 'raw'),
        ('dummy_real_environment_rest.conf', 'REST'),
    ],
)
def test_load_real_environment(conf_file_name, comm_layer_type):
    real_environment_conf = (
        pathlib.Path('arps') / 'test_resources' / 'conf' / conf_file_name
    )
    manager_environment = load_manager_environment(real_environment_conf)
    manager = manager_environment.configuration
    assert not manager_environment.run_as_simulator
    assert 0 == manager_environment.configuration.identifier
    assert (
        pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf'
        == manager.agent_config
    )
    assert {'address': '127.0.0.1', 'port': 1500} == manager.agents_directory
    assert manager.pmt is None
    assert comm_layer_type == manager.comm_layer_type


def test_load_pmt_conf():
    agents_directory = {'address': '127.0.0.1', 'port': 1000}  # doesnt matter
    agent_config = [
        "arps",
        "test_resources",
        "conf",
        "dummy_agent.conf",
    ]  # doesnt matter
    pmt = {'address': '127.0.0.1', 'port': 8000}  # doesnt matter

    with generate_real_env_configuration(
        agent_config, agents_directory, 'raw', pmt
    ) as conf_file_name:
        manager_environment = load_manager_environment(conf_file_name)
        manager = manager_environment.configuration
        assert not manager_environment.run_as_simulator
        assert 0 == manager_environment.configuration.identifier
        assert (
            pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf'
            == manager.agent_config
        )
        assert {'address': '127.0.0.1', 'port': 1000} == manager.agents_directory
        assert {'address': '127.0.0.1', 'port': 8000} == manager.pmt
        assert 'raw' == manager.comm_layer_type


def test_load_wihout_pmt_conf():
    agents_directory = {'address': '127.0.0.1', 'port': 1000}  # doesnt matter
    agent_config = [
        "arps",
        "test_resources",
        "conf",
        "dummy_agent.conf",
    ]  # doesnt matter

    with generate_real_env_configuration(
        agent_config, agents_directory, comm_layer_type='raw'
    ) as conf_file_name:
        manager_environment = load_manager_environment(conf_file_name)
        manager = manager_environment.configuration
        assert not manager_environment.run_as_simulator
        assert 0 == manager_environment.configuration.identifier
        assert (
            pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf'
            == manager.agent_config
        )
        assert {'address': '127.0.0.1', 'port': 1000} == manager.agents_directory
        assert manager.pmt is None
        assert 'raw' == manager.comm_layer_type


def test_load_attribute_failure():
    with pytest.raises(InvalidConfigurationError):
        load_attribute(module_path='', attribute_name='ResourceA')

    with pytest.raises(InvalidConfigurationError):
        load_attribute(
            module_path='arps.test_resources.dummies.dummy_resource', attribute_name=''
        )

    with pytest.raises(InvalidConfigurationError):
        load_attribute(
            module_base_path='..',
            module_path='arps.test_resources.dummies.dummy_resource',
            attribute_name='ResourceA',
        )

    with pytest.raises(InvalidConfigurationError):
        load_attribute(module_path='..dummy_resource', attribute_name='ResourceA')

    with pytest.raises(InvalidConfigurationError):
        load_attribute(
            module_base_path='test_resources.dummies',
            module_path='..dummy_resource',
            attribute_name='ResourceA',
        )


def test_load_attribute_success():
    load_attribute(
        module_path='arps.test_resources.dummies.resources', attribute_name='ResourceA'
    )

    load_attribute(
        module_base_path='arps.test_resources',
        module_path='dummies.resources',
        attribute_name='ResourceA',
    )


if __name__ == '__main__':
    pytest.main([__file__])
