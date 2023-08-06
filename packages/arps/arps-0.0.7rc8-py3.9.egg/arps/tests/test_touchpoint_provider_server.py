import pytest  # type: ignore
import pytest_asyncio

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.clock import simulator_clock_factory
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.payload_factory import PayloadType, create_touchpoint_request
from arps.core.policies.touchpoint_status import TouchPointStatusProviderPolicy
from arps.core.policies_executor import PoliciesExecutor
from arps.core.remove_logger_files import remove_logger_files
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.touchpoint import Actuator, Sensor
from arps.test_resources.dummies.dummy_policy import DummyPolicy
from arps.test_resources.dummies.resources import ResourceA, ResourceB
from arps.test_resources.response_policy import ResponsePolicy


@pytest_asyncio.fixture
async def env_setup():
    resource_a = ResourceA(environment_identifier=0, initial_state=10)
    resource_b = ResourceB(environment_identifier=0, initial_state='ON')
    sensors = [Sensor(resource_a), Sensor(resource_b)]
    actuators = [Actuator(resource_b)]

    environment = Environment(sensors=sensors, actuators=actuators)
    communication_layer = FakeCommunicationLayer()
    agent_factory = AgentFactory(
        environment=environment, communication_layer=communication_layer, metrics_loggers=MetricsLoggers()
    )
    clock = simulator_clock_factory()
    agent_id_manager = AgentIDManager(0)
    sender_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    receiver_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()

    clock.start()
    await communication_layer.start()

    yield clock, agent_factory, sender_id, receiver_id

    communication_layer.unregister_all()
    clock.reset()


@pytest.mark.asyncio
async def test_request_sensor_status(env_setup):
    clock, agent_factory, sender_id, receiver_id = env_setup

    touchpoint_provider = PoliciesExecutor(
        policies=[TouchPointStatusProviderPolicy(), DummyPolicy()],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    touchpoint_provider_agent = agent_factory.create_agent(identifier=sender_id, policies_executor=touchpoint_provider)

    clock.add_listener(touchpoint_provider_agent.run)
    touchpoint_requester = PoliciesExecutor(
        policies=[ResponsePolicy(PayloadType.actuators), ResponsePolicy(PayloadType.sensors)],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    touchpoint_requester_agent = agent_factory.create_agent(
        identifier=receiver_id, policies_executor=touchpoint_requester
    )

    clock.add_listener_low_priority(touchpoint_requester_agent.run)
    assert not touchpoint_requester.policy_action_results

    assert not touchpoint_provider._events_received
    assert not touchpoint_requester._events_received

    message = create_touchpoint_request(
        str(touchpoint_requester_agent.identifier), str(touchpoint_provider_agent.identifier), PayloadType.sensors, None
    )

    await touchpoint_requester_agent.send(message, touchpoint_provider_agent.identifier)

    assert touchpoint_provider._events_received[0] == message
    assert not touchpoint_requester.policy_action_results

    while not touchpoint_provider.policy_action_results:
        await clock.update()
        await clock.wait_for_notified_tasks()

    assert not touchpoint_requester._events_received
    assert touchpoint_provider.policy_action_results

    result = touchpoint_requester.policy_action_results.pop()
    assert result.content.touchpoint['ResourceA'] == 10
    assert result.content.touchpoint['ResourceB'] == 'ON'

    remove_logger_files(touchpoint_provider_agent.metrics_logger.logger)
    remove_logger_files(touchpoint_requester_agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_request_actuator_status(env_setup):
    clock, agent_factory, sender_id, receiver_id = env_setup
    touchpoint_provider = PoliciesExecutor(
        policies=[TouchPointStatusProviderPolicy(), DummyPolicy()],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    touchpoint_provider_agent = agent_factory.create_agent(identifier=sender_id, policies_executor=touchpoint_provider)
    clock.add_listener(touchpoint_provider_agent.run)

    touchpoint_requester = PoliciesExecutor(
        policies=[ResponsePolicy(PayloadType.actuators), ResponsePolicy(PayloadType.sensors)],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    touchpoint_requester_agent = agent_factory.create_agent(
        identifier=receiver_id, policies_executor=touchpoint_requester
    )
    clock.add_listener_low_priority(touchpoint_requester_agent.run)

    assert not touchpoint_requester.policy_action_results

    assert not touchpoint_provider._events_received
    assert not touchpoint_requester._events_received

    message = create_touchpoint_request(
        str(touchpoint_requester_agent.identifier),
        str(touchpoint_provider_agent.identifier),
        PayloadType.actuators,
        None,
    )

    await touchpoint_requester_agent.send(message, touchpoint_provider_agent.identifier)

    assert touchpoint_provider._events_received[0] == message
    assert not touchpoint_requester.policy_action_results

    while not touchpoint_provider.policy_action_results:
        await clock.update()
        await clock.wait_for_notified_tasks()

    assert not touchpoint_requester._events_received, touchpoint_provider.policy_action_results
    assert touchpoint_provider.policy_action_results

    result = touchpoint_requester.policy_action_results.pop()
    assert result.content.touchpoint['ResourceB'] == 'ON'

    remove_logger_files(touchpoint_provider_agent.metrics_logger.logger)
    remove_logger_files(touchpoint_requester_agent.metrics_logger.logger)


if __name__ == '__main__':
    pytest.main([__name__])
