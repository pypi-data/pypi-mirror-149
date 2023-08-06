import asyncio

import pytest  # type: ignore
import pytest_asyncio

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (
    MetaOp,
    PayloadType,
    Request,
    Response,
    request_factory,
)
from arps.core.real.raw_communication_layer import RawCommunicationLayer
from arps.core.real.rest_communication_layer import RESTCommunicationLayer
from arps.test_resources.fake_agents_directory_helper import FakeAgentsDirectoryHelper
from arps.test_resources.simple_entity import SimpleEntity


@pytest_asyncio.fixture(params=(RawCommunicationLayer, RESTCommunicationLayer))
async def entities(request):
    agents_directory_helper = FakeAgentsDirectoryHelper()

    entity_one = SimpleEntity(AgentID(0, 1), agents_directory_helper, request.param)
    await entity_one.communication_layer.start()

    entity_two = SimpleEntity(AgentID(0, 2), agents_directory_helper, request.param)
    await entity_two.communication_layer.start()

    yield entity_one, entity_two

    await entity_two.communication_layer.close()

    await entity_one.communication_layer.close()


@pytest.mark.asyncio
async def test_unsupported_requests(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    periodic_action = Request(first_id, second_id, PayloadType.periodic_action, message_id=None)
    await entity_one.send(periodic_action, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.error
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content == 'payload type not supported'

    assert not entity_two.message.done()


@pytest.mark.asyncio
async def test_info(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    info = request_factory(PayloadType.info, first_id, second_id, message_id=None)
    await entity_one.send(info, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)
    await asyncio.wait_for(entity_two.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.info
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content.sensors == ['CPU']
    assert message_in_first.content.actuators == ['increase_cpu_frequency', 'decrease_cpu_frequency']
    assert message_in_first.content.policies == ['DummyPolicy()', 'AnotherDummyPolicy()']
    assert message_in_first.content.related_agents == ['0.0', '0.1', '0.2']

    message_in_second = entity_two.message.result()
    assert isinstance(message_in_second, Request)
    assert message_in_second.type == PayloadType.info
    assert message_in_second.sender_id == first_id
    assert message_in_second.receiver_id == second_id


@pytest.mark.asyncio
async def test_sensors(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    sensors = request_factory(PayloadType.sensors, first_id, second_id, message_id=None)
    await entity_one.send(sensors, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)
    await asyncio.wait_for(entity_two.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.sensors
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content.touchpoint == {'SensorID': 'sensor_value'}

    message_in_second = entity_two.message.result()
    assert isinstance(message_in_second, Request)
    assert message_in_second.type == PayloadType.sensors
    assert message_in_second.sender_id == first_id
    assert message_in_second.receiver_id == second_id


@pytest.mark.asyncio
async def test_actuators(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    actuators = request_factory(PayloadType.actuators, first_id, second_id, message_id=None)
    await entity_one.send(actuators, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)
    await asyncio.wait_for(entity_two.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.actuators
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content.touchpoint == {'ActuatorID': 'actuator_value'}

    message_in_second = entity_two.message.result()
    assert isinstance(message_in_second, Request)
    assert message_in_second.type == PayloadType.actuators
    assert message_in_second.sender_id == first_id
    assert message_in_second.receiver_id == second_id


@pytest.mark.asyncio
async def test_policy(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    policy_op = {'operation': MetaOp.add.name, 'policy': 'SomePolicy', 'period': None}
    policy = request_factory(PayloadType.policy, first_id, second_id, message_id=None, content=policy_op)
    await entity_one.send(policy, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)
    await asyncio.wait_for(entity_two.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.policy
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content.status == 'Updated successfully'

    message_in_second = entity_two.message.result()
    assert isinstance(message_in_second, Request)
    assert message_in_second.type == PayloadType.policy
    assert message_in_second.sender_id == first_id
    assert message_in_second.receiver_id == second_id


@pytest.mark.asyncio
async def test_meta_agent(entities):
    entity_one, entity_two = entities
    first_id = str(entity_one.identifier)
    second_id = str(entity_two.identifier)

    meta_agent_op = {'operation': MetaOp.add.name, 'to_agent': '0.2'}
    meta_agent = request_factory(PayloadType.meta_agent, first_id, second_id, message_id=None, content=meta_agent_op)
    await entity_one.send(meta_agent, entity_two.identifier)

    await asyncio.wait_for(entity_one.message, timeout=6)
    await asyncio.wait_for(entity_two.message, timeout=6)

    message_in_first = entity_one.message.result()
    assert isinstance(message_in_first, Response)
    assert message_in_first.type == PayloadType.meta_agent
    assert message_in_first.sender_id == second_id
    assert message_in_first.receiver_id == first_id
    assert message_in_first.content.status == 'Updated successfully'

    message_in_second = entity_two.message.result()
    assert isinstance(message_in_second, Request)
    assert message_in_second.type == PayloadType.meta_agent
    assert message_in_second.sender_id == first_id
    assert message_in_second.receiver_id == second_id


if __name__ == '__main__':
    pytest.main([__file__])
