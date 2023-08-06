from collections import Counter

import pytest  # type: ignore

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.clock import simulator_clock_factory
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.mobile_entity import Boundaries, Coordinates
from arps.core.payload_factory import PayloadType, create_info_request
from arps.core.policies.info import InfoProviderPolicy
from arps.core.policies_executor import PoliciesExecutor
from arps.core.remove_logger_files import remove_logger_files
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.touchpoint import Actuator, Sensor
from arps.test_resources.dummies.dummy_policy import DummyPolicy
from arps.test_resources.dummies.resources import ResourceA, ResourceB
from arps.test_resources.response_policy import ResponsePolicy


@pytest.fixture(params=[None, Boundaries(upper=Coordinates(5, 5, 5), lower=Coordinates(0, 0, 0))])
async def env_setup(request):
    resource_a = ResourceA(environment_identifier=0)
    resource_b = ResourceB(environment_identifier=0)
    sensors = [Sensor(resource_a), Sensor(resource_b)]
    actuators = [Actuator(resource_b)]

    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()
    environment = Environment(sensors=sensors, actuators=actuators, boundaries=request.param)
    agent_factory = AgentFactory(
        environment=environment,
        metrics_loggers=MetricsLoggers(),
        communication_layer=comm_layer,
    )

    clock = simulator_clock_factory()
    clock.start()

    agent_id_manager = AgentIDManager(0)
    sender_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    receiver_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()

    yield clock, agent_factory, sender_id, receiver_id

    clock.reset()

    await comm_layer.close()


@pytest.mark.asyncio
async def test_request_info(env_setup):
    clock, agent_factory, sender_id, receiver_id = env_setup

    info_provider = PoliciesExecutor(
        policies=[InfoProviderPolicy(), DummyPolicy()],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    info_provider_agent = agent_factory.create_agent(identifier=sender_id, policies_executor=info_provider)

    clock.add_listener(info_provider_agent.run)

    info_requester = PoliciesExecutor(
        policies=[ResponsePolicy(PayloadType.info)],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )
    info_requester_agent = agent_factory.create_agent(identifier=receiver_id, policies_executor=info_requester)

    clock.add_listener(info_requester_agent.run)

    assert not info_requester.policy_action_results

    assert not info_provider._events_received
    assert not info_requester._events_received

    message = create_info_request(
        str(info_requester_agent.identifier), str(info_provider_agent.identifier), None
    )  # The message id doesn't matter here
    await info_requester_agent.send(message, info_provider_agent.identifier)

    # provider receive the request
    assert info_provider._events_received[0] == message
    assert not info_requester.policy_action_results

    # wait for the results since the order of execution is non-deterministic
    while not info_requester.policy_action_results:
        await clock.update()
        await clock.wait_for_notified_tasks()
    # provider process the request and schedule a response to be executed
    # on the next cycle
    assert not info_provider._events_received
    assert info_requester.policy_action_results[0]

    result = info_requester.policy_action_results.pop()
    assert Counter(result.content.sensors) == Counter(['ResourceA', 'ResourceB'])
    assert Counter(result.content.actuators) == Counter(['ResourceB'])

    if info_provider_agent.coordinates:
        assert result.content.coordinates == Coordinates(0, 0, 0)

    remove_logger_files(info_provider_agent.metrics_logger.logger)
    remove_logger_files(info_requester_agent.metrics_logger.logger)


if __name__ == '__main__':
    pytest.main([__file__])
