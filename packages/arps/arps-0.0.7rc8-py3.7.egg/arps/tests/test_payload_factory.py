'''These tests are just to characterize the behaviour

'''
from dataclasses import asdict

import pytest  # type: ignore

from arps.core.payload_factory import (
    MetaOp,
    PayloadType,
    Request,
    Response,
    create_action_request,
    create_action_response,
    create_info_request,
    create_info_response,
    create_meta_agent_request,
    create_meta_agent_response,
    create_periodic_action,
    create_policy_request,
    create_policy_response,
    create_touchpoint_request,
    create_touchpoint_response,
    request_factory,
    response_factory,
)


@pytest.fixture
def test_parameters():
    sender_id = 0
    receiver_id = 1
    message_id = 'message_id'

    yield sender_id, receiver_id, message_id


def test_info_request_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    info = create_info_request(sender_id, receiver_id, message_id)

    assert isinstance(info, Request)
    assert info.sender_id == sender_id
    assert info.receiver_id == receiver_id
    assert info.type == PayloadType.info
    assert info.message_id == message_id


def test_sensors_request_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    touchpoint = create_touchpoint_request(
        sender_id, receiver_id, PayloadType.sensors, message_id
    )

    assert isinstance(touchpoint, Request)
    assert touchpoint.sender_id == sender_id
    assert touchpoint.receiver_id == receiver_id
    assert touchpoint.type == PayloadType.sensors
    assert touchpoint.message_id == message_id


def test_actuators_request_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    touchpoint = create_touchpoint_request(
        sender_id, receiver_id, PayloadType.actuators, message_id
    )

    assert isinstance(touchpoint, Request)
    assert touchpoint.sender_id == sender_id
    assert touchpoint.receiver_id == receiver_id
    assert touchpoint.type == PayloadType.actuators
    assert touchpoint.message_id == message_id


def test_info_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    sensors = ['CPU']
    actuators = ['increase_cpu_frequency', 'decrease_cpu_frequency']
    policies = ['DummyPolicy()', 'AnotherDummyPolicy()']
    related_agents = ['0.0', '0.1', '0.2']
    info = create_info_response(
        sender_id, receiver_id, message_id, sensors, actuators, policies, related_agents
    )

    assert isinstance(info, Response)
    assert info.sender_id == sender_id
    assert info.receiver_id == receiver_id
    assert info.type == PayloadType.info
    assert info.message_id == message_id
    assert info.content.sensors == sensors
    assert info.content.actuators == actuators
    assert info.content.policies == policies
    assert info.content.related_agents == related_agents


def test_sensors_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    touchpoint = create_touchpoint_response(
        sender_id, receiver_id, PayloadType.sensors, {'CPU': '100'}, message_id
    )

    assert isinstance(touchpoint, Response)
    assert touchpoint.sender_id == sender_id
    assert touchpoint.receiver_id == receiver_id
    assert touchpoint.type == PayloadType.sensors
    assert touchpoint.message_id == message_id
    assert touchpoint.content.touchpoint == {'CPU': '100'}


def test_actuators_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    touchpoint = create_touchpoint_response(
        sender_id,
        receiver_id,
        PayloadType.actuators,
        {
            'CPUFreq': {
                'current_frequency': 2000.0,
                'minimum_frequency_allowed': 800.0,
                'maximum_frequency_allowed': 2900.0,
            }
        },
        message_id,
    )

    assert isinstance(touchpoint, Response)
    assert touchpoint.sender_id == sender_id
    assert touchpoint.receiver_id == receiver_id
    assert touchpoint.type == PayloadType.actuators
    assert touchpoint.message_id == message_id
    assert touchpoint.content.touchpoint == {
        'CPUFreq': {
            'current_frequency': 2000.0,
            'minimum_frequency_allowed': 800.0,
            'maximum_frequency_allowed': 2900.0,
        }
    }


def test_sensors_multiple_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    sensors = create_touchpoint_response(
        sender_id,
        receiver_id,
        PayloadType.sensors,
        {'CPU': '100', 'OtherResource': 'value'},
        message_id,
    )
    assert isinstance(sensors, Response)
    assert sensors.sender_id == sender_id
    assert sensors.receiver_id == receiver_id
    assert sensors.type == PayloadType.sensors
    assert sensors.message_id == message_id
    assert sensors.content.touchpoint == {'CPU': '100', 'OtherResource': 'value'}


def test_policy_request_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    policy = create_policy_request(
        sender_id, receiver_id, MetaOp.add, {'policy': 'SomePolicy'}, message_id
    )

    assert isinstance(policy, Request)
    assert policy.sender_id == sender_id
    assert policy.receiver_id == receiver_id
    assert policy.type == PayloadType.policy
    assert policy.message_id == message_id
    assert policy.content.op == MetaOp.add
    assert policy.content.meta == {'policy': 'SomePolicy'}


def test_policy_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    policy = create_policy_response(
        sender_id, receiver_id, 'status message', message_id
    )

    assert isinstance(policy, Response)
    assert policy.sender_id == sender_id
    assert policy.receiver_id == receiver_id
    assert policy.type == PayloadType.policy
    assert policy.message_id == message_id
    assert policy.content.status == 'status message'


def test_meta_agent_request_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    meta_agent = create_meta_agent_request(
        sender_id, receiver_id, MetaOp.add, '0.1', message_id
    )

    assert isinstance(meta_agent, Request)
    assert meta_agent.sender_id == sender_id
    assert meta_agent.receiver_id == receiver_id
    assert meta_agent.type == PayloadType.meta_agent
    assert meta_agent.message_id == message_id
    assert meta_agent.content.op == MetaOp.add
    assert meta_agent.content.meta == '0.1'


def test_meta_agent_response_creation(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    meta_agent = create_meta_agent_response(
        sender_id, receiver_id, 'status message', message_id
    )

    assert isinstance(meta_agent, Response)
    assert meta_agent.sender_id == sender_id
    assert meta_agent.receiver_id == receiver_id
    assert meta_agent.type == PayloadType.meta_agent
    assert meta_agent.message_id == message_id
    assert meta_agent.content.status == 'status message'


def test_create_periodic_action(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    periodic_action = create_periodic_action(10)
    assert not isinstance(periodic_action, Request)
    assert not isinstance(periodic_action, Response)
    assert periodic_action.sender_id == str(None)
    assert periodic_action.receiver_id == str(None)
    assert periodic_action.type == PayloadType.periodic_action
    assert periodic_action.message_id is None
    assert periodic_action.content == 10


def test_create_action_request(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    action = create_action_request(sender_id, receiver_id, 'commit crime', message_id)
    assert isinstance(action, Request)
    assert action.sender_id == sender_id
    assert action.receiver_id == receiver_id
    assert action.type == PayloadType.action
    assert action.message_id == message_id
    assert action.content.action == 'commit crime'


def test_create_action_response(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    action = create_action_response(sender_id, receiver_id, 'nope', message_id)
    assert isinstance(action, Response)
    assert action.sender_id == sender_id
    assert action.receiver_id == receiver_id
    assert action.type == PayloadType.action
    assert action.message_id == message_id
    assert action.content.status == 'nope'


# To dict


def test_dict_from_request(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    info = create_info_request(sender_id, receiver_id, message_id)
    assert isinstance(info, Request)
    assert asdict(info) == {
        'message_id': 'message_id',
        'receiver_id': 1,
        'sender_id': 0,
        'type': PayloadType.info,
        'content': None,
    }


def test_dict_from_response(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    sensors = ['CPU']
    actuators = ['increase_cpu_frequency', 'decrease_cpu_frequency']
    policies = ['DummyPolicy()', 'AnotherDummyPolicy()']
    related_agents = ['0.0', '0.1', '0.2']
    info = create_info_response(
        sender_id, receiver_id, message_id, sensors, actuators, policies, related_agents
    )

    assert asdict(info) == {
        'content': {
            'actuators': ['increase_cpu_frequency', 'decrease_cpu_frequency'],
            'policies': ['DummyPolicy()', 'AnotherDummyPolicy()'],
            'related_agents': ['0.0', '0.1', '0.2'],
            'sensors': ['CPU'],
        },
        'message_id': 'message_id',
        'receiver_id': 1,
        'sender_id': 0,
        'type': PayloadType.info,
    }


# Request Factory


def test_request_factory_info(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_info_request(sender_id, receiver_id, message_id)
    created = request_factory(PayloadType.info, sender_id, receiver_id, message_id)
    assert expected == created


def test_request_factory_sensors(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_touchpoint_request(
        sender_id, receiver_id, PayloadType.sensors, message_id
    )

    created = request_factory(PayloadType.sensors, sender_id, receiver_id, message_id)
    assert expected == created


def test_request_factory_actuators(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_touchpoint_request(
        sender_id, receiver_id, PayloadType.actuators, message_id
    )

    created = request_factory(PayloadType.actuators, sender_id, receiver_id, message_id)
    assert expected == created


def test_request_factory_policy(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_policy_request(
        sender_id, receiver_id, MetaOp.add, {'policy': 'SomePolicy'}, message_id
    )

    created = request_factory(
        PayloadType.policy,
        sender_id,
        receiver_id,
        message_id,
        {'operation': 'add', 'policy': 'SomePolicy'},
    )

    assert expected == created


def test_request_factory_periodic_policy(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_policy_request(
        sender_id,
        receiver_id,
        MetaOp.add,
        {'policy': 'SomePolicy', 'period': 1},
        message_id,
    )

    created = request_factory(
        PayloadType.policy,
        sender_id,
        receiver_id,
        message_id,
        {'operation': 'add', 'policy': 'SomePolicy', 'period': 1},
    )

    assert expected == created


def test_request_factory_meta_agent(test_parameters):

    sender_id, receiver_id, message_id = test_parameters
    expected = create_meta_agent_request(
        sender_id, receiver_id, MetaOp.add, str(sender_id), message_id
    )

    meta_agent_op = {'operation': 'add', 'to_agent': str(sender_id)}
    created = request_factory(
        PayloadType.meta_agent, sender_id, receiver_id, message_id, meta_agent_op
    )

    assert expected == created


def test_request_factory_action(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_action_request(sender_id, receiver_id, 'some action', message_id)

    created = request_factory(
        PayloadType.action, sender_id, receiver_id, message_id, 'some action'
    )

    assert expected == created


def test_request_factory_fail_payload_type(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    with pytest.raises(ValueError):
        request_factory('wrong', sender_id, receiver_id, message_id)


def test_request_factory_fail_required_args(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    with pytest.raises(ValueError):
        request_factory(PayloadType.meta_agent, sender_id, receiver_id, message_id)


# Response Factory


def test_response_factory_info(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    sensors = ['CPU']
    actuators = ['increase_cpu_frequency', 'decrease_cpu_frequency']
    policies = ['DummyPolicy()', 'AnotherDummyPolicy()']
    related_agents = ['0.0', '0.1', '0.2']
    content = (sensors, actuators, policies, related_agents)

    expected = create_info_response(
        sender_id, receiver_id, message_id, sensors, actuators, policies, related_agents
    )
    created = response_factory(
        PayloadType.info, sender_id, receiver_id, message_id, content
    )
    assert expected == created


def test_response_factory_info_with_coordinates(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    sensors = ['CPU']
    actuators = ['increase_cpu_frequency', 'decrease_cpu_frequency']
    policies = ['DummyPolicy()', 'AnotherDummyPolicy()']
    related_agents = ['0.0', '0.1', '0.2']
    coordinates = (1, 2, 3)
    content = (sensors, actuators, policies, related_agents)

    expected = create_info_response(
        sender_id,
        receiver_id,
        message_id,
        sensors,
        actuators,
        policies,
        related_agents,
        coordinates,
    )
    created = response_factory(
        PayloadType.info, sender_id, receiver_id, message_id, content
    )
    assert expected == created


def test_response_factory_sensors(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    content = {'sensorA': 'value'}
    expected = create_touchpoint_response(
        sender_id, receiver_id, PayloadType.sensors, content, message_id
    )

    created = response_factory(
        PayloadType.sensors, sender_id, receiver_id, message_id, content
    )
    assert expected == created


def test_response_factory_actuators(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    content = {'actuatorA': 'value'}
    expected = create_touchpoint_response(
        sender_id, receiver_id, PayloadType.actuators, content, message_id
    )

    created = response_factory(
        PayloadType.actuators, sender_id, receiver_id, message_id, content
    )
    assert expected == created


def test_response_factory_policy(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_policy_response(
        sender_id, receiver_id, 'policy response', message_id
    )

    created = response_factory(
        PayloadType.policy, sender_id, receiver_id, message_id, 'policy response'
    )

    assert expected == created


def test_response_factory_meta_agent(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_meta_agent_response(
        sender_id, receiver_id, 'meta agent response', message_id
    )

    created = response_factory(
        PayloadType.meta_agent,
        sender_id,
        receiver_id,
        message_id,
        'meta agent response',
    )

    assert expected == created


def test_response_factory_action(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    expected = create_action_response(sender_id, receiver_id, 'some action', message_id)

    created = response_factory(
        PayloadType.action, sender_id, receiver_id, message_id, 'some action'
    )
    assert expected == created


def test_response_factory_fail_payload_type(test_parameters):
    sender_id, receiver_id, message_id = test_parameters
    with pytest.raises(ValueError):
        response_factory('wrong', sender_id, receiver_id, message_id, 'content')


if __name__ == '__main__':
    pytest.main([__file__])
