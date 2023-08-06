import asyncio
import contextlib
from collections import Counter

import pytest # type: ignore

from arps.core.touchpoint import Sensor, Actuator
from arps.core.environment import Environment
from arps.core.payload_factory import PayloadType
from arps.core.agent_id_manager import AgentID

from arps.test_resources.dummies.resources import (ResourceA,
                                                   ResourceB,
                                                   ReceivedMessagesResource)
from arps.test_resources.dummies.dummy_policy import (DummyPolicy,
                                                      SenderPolicy,
                                                      ReceiverPolicy,
                                                      CollectResponsePolicy)

from arps.test_resources.agent_interaction_helper import (setup_agent_handler,
                                                          real_env_components)

from arps.apps.client import AgentClient
from arps.core.real.rest_api_utils import random_port

# pylint: disable-msg=redefined-outer-name


@contextlib.asynccontextmanager
async def setup_agent(agent_id, policies, test_env):
    clock, agents_directory_helper, comm_layer_cls = test_env

    comm_logger_resource = ReceivedMessagesResource(environment_identifier=0)
    resource_a = ResourceA(environment_identifier=0, initial_state=10)
    resource_b = ResourceB(environment_identifier=0, initial_state='OFF')
    environment = Environment(sensors=[Sensor(resource_a), Sensor(resource_b)],
                              actuators=[Actuator(resource_b),
                                         Actuator(resource=comm_logger_resource)])
    with setup_agent_handler(policies, environment, clock,
                             agent_id, agents_directory_helper,
                             comm_layer_cls) as agent_handler:

        await agent_handler.start()

        yield agent_handler

        await agent_handler.finalize()


@contextlib.asynccontextmanager
async def setup_client(test_env):
    clock, agents_directory_helper, comm_layer_cls = test_env

    comm_layer = comm_layer_cls(random_port(), agents_directory_helper)

    await comm_layer.start()
    agent_client = AgentClient(AgentID(0, 0), comm_layer)

    yield agent_client

    await agent_client.finalize()

    await comm_layer.close()


@pytest.mark.asyncio
async def test_info_client_single_agent_interaction(real_env_components):
    agent_id = AgentID(0, 1)

    # DummyPolicy is necessary to test if the sensors are loaded correctly
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(setup_agent(agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))
        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        info = await agent_client.send_request(agent_id, PayloadType.info)

        assert info.receiver_id == str(agent_client.identifier)
        assert info.type == PayloadType.info
        assert info.sender_id == str(agent_id)
        assert Counter(info.content.sensors) == Counter(['ResourceA', 'ResourceB'])
        assert Counter(info.content.actuators) == Counter(['ResourceB', 'ReceivedMessagesResource'])


@pytest.mark.asyncio
async def test_info_client_multiple_agents_interaction(real_env_components):
    agent_id = AgentID(0, 1)
    another_agent_id = AgentID(0, 2)

    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(setup_agent(agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        await stack.enter_async_context(setup_agent(another_agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        info = await agent_client.send_request(agent_id, PayloadType.info)

        assert info.receiver_id == str(agent_client.identifier)
        assert info.type == PayloadType.info
        assert info.sender_id == str(agent_id)
        assert Counter(info.content.sensors) == Counter(['ResourceA', 'ResourceB'])
        assert Counter(info.content.actuators) == Counter(['ResourceB', 'ReceivedMessagesResource'])

        response = await agent_client.send_request(another_agent_id, PayloadType.info)

        assert response.receiver_id == str(agent_client.identifier)
        assert response.type == PayloadType.info
        assert response.sender_id == str(another_agent_id)
        assert Counter(response.content.sensors) == Counter(['ResourceA', 'ResourceB'])
        assert Counter(response.content.actuators) == Counter(['ResourceB', 'ReceivedMessagesResource'])


@pytest.mark.asyncio
async def test_sensors_client_single_agent_interaction(real_env_components):
    agent_id = AgentID(0, 1)

    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(setup_agent(agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        sensor = await agent_client.send_request(agent_id, PayloadType.sensors)

        assert sensor.type == PayloadType.sensors
        assert sensor.content.touchpoint['ResourceA'] == 10
        assert sensor.content.touchpoint['ResourceB'] == 'OFF'


@pytest.mark.asyncio
async def test_sensors_client_multiple_agents_interaction(real_env_components):
    agent_id = AgentID(0, 1)
    another_agent_id = AgentID(0, 2)

    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(setup_agent(agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        await stack.enter_async_context(setup_agent(another_agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        sensor = await agent_client.send_request(agent_id, PayloadType.sensors)
        assert sensor.type == PayloadType.sensors
        assert sensor.content.touchpoint['ResourceA'] == 10
        assert sensor.content.touchpoint['ResourceB'] == 'OFF'

        sensor = await agent_client.send_request(another_agent_id, PayloadType.sensors)
        assert sensor.type == PayloadType.sensors
        assert sensor.content.touchpoint['ResourceA'] == 10
        assert sensor.content.touchpoint['ResourceB'] == 'OFF'


@pytest.mark.asyncio
async def test_actuators_client_single_agent_interaction(real_env_components):
    agent_id = AgentID(0, 1)

    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(setup_agent(agent_id,
                                                    {DummyPolicy: None},
                                                    real_env_components))

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        actuator = await agent_client.send_request(agent_id, PayloadType.actuators)
        assert actuator.type == PayloadType.actuators
        assert actuator.content.touchpoint['ResourceB'] == 'OFF'


@pytest.mark.asyncio
async def test_agent_relationship(real_env_components):
    agent_id = AgentID(0, 1)
    other_agent_id = AgentID(0, 2)

    async with contextlib.AsyncExitStack() as stack:
        agent_handler = await stack.enter_async_context(setup_agent(agent_id,
                                                                    {SenderPolicy: 10,
                                                                     CollectResponsePolicy: None},
                                                                    real_env_components))

        other_handler = await stack.enter_async_context(setup_agent(other_agent_id,
                                                                    {ReceiverPolicy: None},
                                                                    real_env_components))
        agent = agent_handler.agent
        other_agent = other_handler.agent
        assert not len(agent.related_agents)
        assert not len(other_agent.related_agents)

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'add', 'to_agent': str(other_agent_id)})
        assert response.content.status == f'Operation include_as_related of {other_agent_id} performed in {agent_id}'

        assert agent.related_agents == {other_agent.identifier}
        assert not len(other_agent.related_agents)

        while agent_handler.clock.epoch_time.epoch < 30:
            # this means that agents will interact at least once
            await asyncio.sleep(0)

        assert len(agent.policies_executor.policy_action_results) <= 2

        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'remove', 'to_agent': str(other_agent_id)})
        assert response.content.status == f'Operation remove_as_related of {other_agent_id} performed in {agent_id}'


@pytest.mark.asyncio
async def test_agent_relationship_with_non_existent_agent(real_env_components):
    agent_id = AgentID(0, 1)
    other_agent_id = AgentID(0, 2)
    non_existent_agent_id = AgentID(0, 3)

    async with contextlib.AsyncExitStack() as stack:
        agent_handler = await stack.enter_async_context(setup_agent(agent_id,
                                                                    {SenderPolicy: 3,
                                                                     CollectResponsePolicy: None},
                                                                    real_env_components))

        agent = agent_handler.agent
        other_handler = await stack.enter_async_context(setup_agent(other_agent_id,
                                                                    {ReceiverPolicy: None},
                                                                    real_env_components))
        agent = agent_handler.agent
        other_agent = other_handler.agent
        assert not len(agent.related_agents)
        assert not len(other_agent.related_agents)

        agent_client = await stack.enter_async_context(setup_client(real_env_components))

        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'add', 'to_agent': str(other_agent_id)})
        assert response.content.status == f'Operation include_as_related of {other_agent_id} performed in {agent_id}'
        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'add', 'to_agent': str(non_existent_agent_id)})
        assert response.content.status == f'Operation include_as_related of {non_existent_agent_id} performed in {agent_id}'

        while agent_handler.clock.epoch_time.epoch < 10:
            # this means that agents will interact at least once
            await asyncio.sleep(0)

        # Removing relationshup to avoid communication error during test teardown
        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'remove', 'to_agent': str(other_agent_id)})
        assert response.content.status == f'Operation remove_as_related of {other_agent_id} performed in {agent_id}'
        response = await agent_client.send_request(agent.identifier,
                                                   PayloadType.meta_agent,
                                                   content={'operation': 'remove', 'to_agent': str(non_existent_agent_id)})
        assert response.content.status == f'Operation remove_as_related of {non_existent_agent_id} performed in {agent_id}'

        error_result = next(result for result in agent.policies_executor.policy_action_results if result.type == PayloadType.error)
        valid_result = next(result for result in agent.policies_executor.policy_action_results if result.type == PayloadType.action)

        assert 'Agent 0.3 not found' == error_result.content
        assert 'Executed action requested by 0.1' == valid_result.content.status


if __name__ == '__main__':
    pytest.main([__file__])
