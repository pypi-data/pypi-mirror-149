import pytest # type: ignore

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.environment import Environment
from arps.core.clock import simulator_clock_factory
from arps.core.metrics_logger import MetricsLoggers
from arps.core.payload_factory import (PayloadType,
                                       create_policy_request,
                                       Request,
                                       MetaOp)
from arps.core.policies.meta import MetaPolicyProvider
from arps.core.policies_executor import PoliciesExecutor

from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer

from arps.test_resources.dummies.dummy_policy import (DummyPolicy,
                                                      DummyPeriodicPolicy)
from arps.core.remove_logger_files import remove_logger_files


async def abstract_factory(environment=None):
    environment = environment or Environment(sensors=[], actuators=[])
    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()

    return AgentFactory(environment=environment,
                        metrics_loggers=MetricsLoggers(),
                        communication_layer=comm_layer)


@pytest.fixture
async def env_setup():
    clock = simulator_clock_factory()
    agent_id_manager = AgentIDManager(0)
    sender_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    receiver_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    message_id = 'message_id'

    clock.start()

    yield clock, sender_id, receiver_id, message_id, abstract_factory

    clock.reset()


@pytest.mark.asyncio
async def test_add_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup

    policies_executor = PoliciesExecutor(policies=[MetaPolicyProvider()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPolicy', DummyPolicy)

    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    await agent.receive(create_policy_request(str(sender_id),
                                              str(receiver_id),
                                              MetaOp.add,
                                              {'policy': 'DummyPolicy'},
                                              message_id))

    assert 1 == len(agent.policies_executor._policies)

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert 2 == len(agent.policies_executor._policies)

    request = Request(str(sender_id), str(receiver_id), PayloadType.info, 'dummy')
    await agent.receive(request)

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert agent.policies_executor.policy_action_results[0] == request
    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_remove_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPolicy', DummyPolicy)
    policies_executor = PoliciesExecutor(
        policies=[MetaPolicyProvider(), DummyPolicy()],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface)

    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    assert 2 == len(agent.policies_executor._policies)

    await agent.receive(create_policy_request('0.1', '0.0',
                                              MetaOp.remove,
                                              {'policy': 'DummyPolicy'},
                                              message_id))

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert 1 == len(agent.policies_executor._policies)

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_remove_mandatory_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPolicy', DummyPolicy)
    policies_executor = PoliciesExecutor(
        policies=[MetaPolicyProvider(), DummyPolicy()],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface)

    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    inspected_received_message = []

    async def wrapped_send(message, *_):
        inspected_received_message.append(message)
    agent.communication_layer.send = wrapped_send

    clock.add_listener_low_priority(agent.run)

    assert 2 == len(agent.policies_executor._policies)

    await agent.receive(create_policy_request('0.1', '0.0',
                                              MetaOp.remove,
                                              {'policy': 'MetaPolicyProvider'},
                                              message_id))

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert 2 == len(agent.policies_executor._policies)

    assert inspected_received_message[0].type == PayloadType.error
    assert inspected_received_message[0].content == 'policy MetaPolicyProvider not registered'

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_add_periodic_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup

    policies_executor = PoliciesExecutor(policies=[MetaPolicyProvider()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPeriodicPolicy', DummyPeriodicPolicy)

    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    await agent.receive(create_policy_request(str(sender_id),
                                              str(receiver_id),
                                              MetaOp.add,
                                              {'policy': 'DummyPeriodicPolicy', 'period': 1},
                                              message_id))

    assert 1 == len(agent.policies_executor._policies)

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert 2 == len(agent.policies_executor._policies)

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert len(agent.policies_executor.policy_action_results)
    periodic_event = agent.policies_executor.policy_action_results[0]
    assert periodic_event.type == PayloadType.periodic_action

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_remove_periodic_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPeriodicPolicy', DummyPeriodicPolicy)
    periodic_policy = DummyPeriodicPolicy()
    periodic_policy.period = 1
    policies_executor = PoliciesExecutor(
        policies=[MetaPolicyProvider(), periodic_policy],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface)

    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    assert len(clock._high_listeners) == 1
    assert len(clock._low_listeners) == 1

    assert 2 == len(agent.policies_executor._policies)

    await agent.receive(create_policy_request('0.1', '0.0', MetaOp.remove,
                                              {'policy': 'DummyPeriodicPolicy'}, message_id))

    await clock.update()
    await clock.wait_for_notified_tasks()

    assert 1 == len(agent.policies_executor._policies)

    assert len(clock._high_listeners) == 0
    assert len(clock._low_listeners) == 1

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_unknown_policy(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup
    policies_executor = PoliciesExecutor(policies=[MetaPolicyProvider()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    agent_factory = await abstract_factory()
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    await agent.receive(create_policy_request(str(receiver_id),
                                              str(sender_id),
                                              MetaOp.add,
                                              {'policy': 'DummyPolicyTypo'},
                                              message_id))

    assert 1 == len(agent.policies_executor._policies)

    inspected_received_message = []

    async def wrapped_send(message, *_):
        inspected_received_message.append(message)
    agent.communication_layer.send = wrapped_send

    await clock.update()
    await clock.wait_for_notified_tasks()

    response = inspected_received_message[0]
    assert response.sender_id == str(sender_id)
    assert response.receiver_id == str(receiver_id)
    assert response.type == PayloadType.error
    assert response.message_id == message_id
    assert response.content == 'policy DummyPolicyTypo not registered'

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_unknwon_operation(env_setup):
    clock, sender_id, receiver_id, message_id, abstract_factory = env_setup
    policies_executor = PoliciesExecutor(policies=[MetaPolicyProvider()],
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    environment = Environment(sensors=[], actuators=[])
    environment.register_policy('DummyPolicy', DummyPolicy)
    agent_factory = await abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=sender_id, policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)

    await agent.receive(create_policy_request(str(receiver_id),
                                              str(sender_id), 255,
                                              {'policy': 'DummyPolicy'},
                                              message_id))

    assert 1 == len(agent.policies_executor._policies)

    inspected_received_message = []

    async def wrapped_send(message, *_):
        inspected_received_message.append(message)
    agent.communication_layer.send = wrapped_send

    await clock.update()
    await clock.wait_for_notified_tasks()

    response = inspected_received_message[0]
    assert response.sender_id == str(sender_id)
    assert response.receiver_id == str(receiver_id)
    assert response.type == PayloadType.error
    assert response.message_id == message_id
    assert response.content == 'unknown operation code 255'

    remove_logger_files(agent.metrics_logger.logger)


if __name__ == '__main__':
    pytest.main([__file__])
