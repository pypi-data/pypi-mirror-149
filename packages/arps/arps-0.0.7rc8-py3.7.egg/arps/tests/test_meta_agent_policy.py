import pytest # type: ignore

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentID
from arps.core.environment import Environment
from arps.core.clock import simulator_clock_factory
from arps.core.metrics_logger import MetricsLoggers
from arps.core.payload_factory import (PayloadType,
                                       create_meta_agent_request,
                                       MetaOp)
from arps.core.policies.meta_agent import MetaAgentProviderPolicy
from arps.core.policies_executor import PoliciesExecutor

from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer

from arps.test_resources.response_policy import ResponsePolicy
from arps.core.remove_logger_files import remove_logger_files

#################################
# MetaAgentProviderPolicy tests #
#################################


@pytest.fixture
async def env_setup():
    clock = simulator_clock_factory()
    policies_executor = PoliciesExecutor(policies=[MetaAgentProviderPolicy()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    environment = Environment(sensors={}, actuators={})
    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()

    sender_id = AgentID(0, 0)
    another_agent_id = AgentID(0, 1)
    message_id = 0
    agent_factory = AgentFactory(environment=environment,
                                 metrics_loggers=MetricsLoggers(),
                                 communication_layer=comm_layer)
    agent = agent_factory.create_agent(identifier=sender_id,
                                       policies_executor=policies_executor)

    clock.add_listener(agent.run)

    clock.start()

    yield clock, agent, sender_id, another_agent_id, message_id

    remove_logger_files(agent.metrics_logger.logger)

    clock.reset()


@pytest.mark.asyncio
async def test_add_agent(env_setup):
    clock, agent, sender_id, another_agent_id, message_id = env_setup

    await agent.receive(create_meta_agent_request(str(sender_id),
                                                  str(sender_id),
                                                  MetaOp.add,
                                                  str(another_agent_id),
                                                  message_id))

    assert not agent.related_agents

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert agent.related_agents
    assert another_agent_id in agent.related_agents


@pytest.mark.asyncio
async def test_remove_agent(env_setup):
    clock, agent, sender_id, another_agent_id, message_id = env_setup
    agent.include_as_related(another_agent_id)

    await agent.receive(create_meta_agent_request(str(sender_id),
                                                  str(sender_id),
                                                  MetaOp.remove,
                                                  str(another_agent_id),
                                                  message_id))

    assert agent.related_agents
    await clock.update()
    await clock.wait_for_notified_tasks()
    assert not agent.related_agents


@pytest.mark.asyncio
async def test_unknown_operation(env_setup):
    clock, agent, sender_id, another_agent_id, message_id = env_setup
    await agent.receive(create_meta_agent_request(str(sender_id),
                                                  str(sender_id),
                                                  'SomeUnknownOP',
                                                  str(another_agent_id),
                                                  message_id))

    assert not agent.related_agents

    inspected_received_message = []

    async def send(message, *_):
        inspected_received_message.append(message)
    agent.communication_layer.send = send

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert not agent.related_agents

    response = inspected_received_message[0]
    assert response.sender_id == str(sender_id)
    assert response.receiver_id == str(sender_id)
    assert response.type == PayloadType.meta_agent
    assert response.message_id == message_id
    assert response.content.status == 'unknown operation code SomeUnknownOP'


####################################
# MetaAgent policies workflow test #
####################################

@pytest.mark.asyncio
async def test_event_processed_successfully():
    clock = simulator_clock_factory()

    environment = Environment(sensors={}, actuators={})
    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()

    client_agent_id = AgentID(0, 0)
    agent_id = AgentID(0, 1)

    agent_factory = AgentFactory(environment=environment,
                                 metrics_loggers=MetricsLoggers(),
                                 communication_layer=comm_layer)
    policies_executor = PoliciesExecutor(policies=[MetaAgentProviderPolicy()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)
    agent = agent_factory.create_agent(identifier=agent_id,
                                       policies_executor=policies_executor)

    clock.add_listener(agent.run)

    policies_executor = PoliciesExecutor(policies=[ResponsePolicy(PayloadType.meta_agent)],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)
    client_agent = agent_factory.create_agent(identifier=client_agent_id,
                                              policies_executor=policies_executor)
    clock.add_listener(client_agent.run)

    clock.start()

    # add some agent 0.2 into agent 0.1
    message = create_meta_agent_request(sender_id=str(client_agent_id),
                                        receiver_id=str(agent_id),
                                        operation=MetaOp.add,
                                        agents_id='0.2',
                                        message_id=None)
    await client_agent.send(message, agent_id)

    assert agent.policies_executor._events_received
    assert not client_agent.policies_executor.policy_action_results

    # wait for the results since the order of execution is non-deterministic
    while not client_agent.policies_executor.policy_action_results:
        await clock.update()
        await clock.wait_for_notified_tasks()

    assert not agent.policies_executor._events_received
    assert client_agent.policies_executor.policy_action_results

    response = client_agent.policies_executor.policy_action_results.pop()
    assert response.sender_id == str(agent_id)
    assert response.receiver_id == str(client_agent_id)
    assert response.content.status == 'Operation include_as_related of 0.2 performed in 0.1'

    remove_logger_files(client_agent.metrics_logger.logger)
    remove_logger_files(agent.metrics_logger.logger)

if __name__ == '__main__':
    pytest.main([__file__])
