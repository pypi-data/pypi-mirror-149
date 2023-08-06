import logging
import pathlib

import pytest  # type: ignore

from arps.core.agent_id_manager import AgentID, AgentIDManager
from arps.core.clock import simulator_clock_factory
from arps.core.payload_factory import PayloadType
from arps.core.simulator.resource import TrackedValue, EvtType
from arps.core.simulator.simulator import Simulator
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer

from arps.test_resources.dummies.dummy_event_factory import DummySimEvent

from arps.apps.configuration_file_loader import load_manager_environment
from arps.apps.simulator_environment_agent_manager import SimulatorEnvironmentAgentManager


class AppFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        self.epoch_time = kwargs.pop('epoch_time', None)
        super().__init__(*args, **kwargs)

    def filter(self, record):
        record.epoch = f'{self.epoch_time.epoch!r}'
        return True


def assert_sensor(expected_value, result, sender_id, receiver_id):
    assert_result(expected_value, result, sender_id, receiver_id, PayloadType.sensors)


def assert_actuator(expected_value, result, sender_id, receiver_id):
    assert_result(expected_value, result, sender_id, receiver_id, PayloadType.actuators)


def assert_result(expected_value, result, sender_id, receiver_id, message_type):
    assert result.type == message_type
    assert result.sender_id == str(sender_id)
    assert result.receiver_id == str(receiver_id)
    assert result.content.touchpoint == expected_value


@pytest.mark.asyncio
async def test_simulation_single_agent_spawned():
    '''This test is a bit more complex, hence this description.

        The agent manager is reading Sensor(ResourceA) and controlling
        Actuator(ResourceC) Policy at the moment is
        DummyPolicyWithBehavior: if Sensor.read() > 11, action will be
        performed, i. e., resource controlled by Actuator(ResourceC)
        will change to 1.

        The simulation receives two events in the event queue: at
        epoch 5 and at epoch 7

        At epoch 5, resource will be changed to 10, thus
        Sensor(ResourceA) will read 10.  The actuator is the same
        because the Condition in Policy it not met (sensor.read() >
        11).

        At epoch 7, resource will be changed to 25, thus
        Actuator(ResourceC) will read 25.  Now, condition is met and
        Actuator change its resource to 1.

        The remaining time of both tasks was calculated so the tasks
        would keep their values through the tests

    '''

    conf = pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_simulator_environment.conf'
    manager_environment = load_manager_environment(conf)
    assert manager_environment.run_as_simulator
    manager_configuration = manager_environment.configuration[0]

    resources_table = manager_environment.resources_table
    estimators_table = manager_environment.event_queue_loader.event_factory.estimators_table

    event_queue = [DummySimEvent(identifier=1,
                                 arrival_time=5,
                                 remaining_time=4,
                                 resources_table=resources_table,
                                 estimators_table=estimators_table,
                                 modifier=10),
                   DummySimEvent(identifier=2,
                                 arrival_time=7,
                                 remaining_time=10,
                                 resources_table=resources_table,
                                 estimators_table=estimators_table,
                                 modifier=25)]

    clock = simulator_clock_factory()

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(epoch)s : %(levelname)s -  %(name)s : %(message)s')
    handler.setFormatter(formatter)
    handler.addFilter(AppFilter(epoch_time=clock.epoch_time))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    comm_layer = FakeCommunicationLayer()

    agent_mgr = SimulatorEnvironmentAgentManager(manager_configuration=manager_configuration,
                                                 communication_layer=comm_layer,
                                                 clock=clock)
    await agent_mgr.start()

    sim_event_scheduler = manager_environment.sim_event_scheduler
    simulator = Simulator(event_queue, sim_event_scheduler)
    clock.add_listener(simulator.step)

    resources_from_touchpoints = agent_mgr.environment.resources()
    resources_from_touchpoints['ResourceA'].value = TrackedValue(0, 0, None, EvtType.des_main)
    resources_from_touchpoints['ResourceB'].value = TrackedValue('ON', 0, None, EvtType.des_main)
    resources_from_touchpoints['ResourceC'].value = TrackedValue(0, 0, None, EvtType.des_main)

    assert 'ResourceA' in agent_mgr.environment.sensors
    assert 'ResourceB' in agent_mgr.environment.sensors
    assert 'ResourceB' in agent_mgr.environment.actuators

    assert agent_mgr.environment.sensor('ResourceA').read() == 0
    assert agent_mgr.environment.sensor('ResourceB').read() == 'ON'
    assert agent_mgr.environment.actuator('ResourceB').read() == 'ON'
    assert agent_mgr.environment.actuator('ResourceC').read() == 0

    clock.start()

    assert 0 == clock.epoch_time.epoch
    await clock.update()  # start
    assert 1 == clock.epoch_time.epoch

    result = agent_mgr.list_agents()
    assert result == {'agents': []}

    # this will make DummyPolicyWithBehavior required touchpoints
    # be available to be executed Using agents_status
    result = await agent_mgr.spawn_agent(policies={'DummyPolicyWithBehavior': 1})
    assert result == 'Agent 0.1 created'

    agent_id_manager = AgentIDManager(0)

    provider_identifier = agent_id_manager.next_available_id()
    agent_id_manager.commit()

    result = agent_mgr.list_agents()
    assert result == {'agents': [str(provider_identifier)]}

    client_id = AgentID(0, 0)

    def run_coro(coro):
        try:
            result = coro.send(None)
            return result.done()
        except StopIteration as coro_return:
            return coro_return.value

    async def run_touchpoint_requester(*, epoch, sensor, actuator):
        '''
            Executes sensor and actuators request task and run des and mas coro
        '''
        sensors_coro = agent_mgr.agents_status(request_type=PayloadType.sensors,
                                               provider=provider_identifier)

        assert not run_coro(sensors_coro)

        actuators_coro = agent_mgr.agents_status(request_type=PayloadType.actuators,
                                                 provider=provider_identifier)

        assert not run_coro(actuators_coro)

        await clock.update()

        await clock.wait_for_notified_tasks()

        assert epoch + 1 == clock.epoch_time.epoch

        await clock.update()

        await clock.wait_for_notified_tasks()

        assert epoch + 2 == clock.epoch_time.epoch

        await clock.update()

        await clock.wait_for_notified_tasks()

        assert epoch + 3 == clock.epoch_time.epoch

        await clock.update()

        await clock.wait_for_notified_tasks()

        assert epoch + 4 == clock.epoch_time.epoch

        sensor_result = run_coro(sensors_coro)
        assert_sensor(sensor, sensor_result, sender_id=provider_identifier,
                      receiver_id=client_id)

        actuator_result = run_coro(actuators_coro)
        assert_actuator(actuator, actuator_result, sender_id=provider_identifier,
                        receiver_id=client_id)

    await run_touchpoint_requester(epoch=1, sensor={'ResourceA': 0, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'},
                                   actuator={'ResourceB': 'ON', 'ResourceC': 0, 'ReceivedMessagesResource': 0})
    await run_touchpoint_requester(epoch=5, sensor={'ResourceA': 10, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'},
                                   actuator={'ResourceB': 'ON', 'ResourceC': 0, 'ReceivedMessagesResource': 0})
    await run_touchpoint_requester(epoch=9, sensor={'ResourceA': 25, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'},
                                   actuator={'ResourceB': 'ON', 'ResourceC': 4, 'ReceivedMessagesResource': 0})
    await run_touchpoint_requester(epoch=13, sensor={'ResourceA': 25, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'},
                                   actuator={'ResourceB': 'ON', 'ResourceC': 8, 'ReceivedMessagesResource': 0})


if __name__ == '__main__':
    pytest.main([__file__])
