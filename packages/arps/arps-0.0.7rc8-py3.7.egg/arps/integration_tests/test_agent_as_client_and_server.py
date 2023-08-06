from collections import defaultdict
from collections import namedtuple
import logging
import contextlib
import asyncio
import platform
import time
import pathlib

import pytest # type: ignore

from arps.core.agent_id_manager import AgentID
from arps.core.environment import Environment
from arps.core import logger_setup
from arps.core.clock import simulator_clock_factory
from arps.core.payload_factory import PayloadType
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.touchpoint import Actuator

from arps.apps.simulator_environment_agent_manager import SimulatorEnvironmentAgentManager
from arps.apps.real_environment_agent_manager import RealEnvironmentAgentManager

from arps.test_resources.dummies.dummy_policy import (SenderPolicy,
                                                      ReceiverPolicy)
from arps.test_resources.dummies.resources import ReceivedMessagesResource
from arps.test_resources.apps_runner import (start_agents_directory,
                                             remove_process_files)
from arps.core.remove_logger_files import remove_logger_files


@contextlib.contextmanager
def sim_environment():
    received_messages_resource = ReceivedMessagesResource(environment_identifier=0)
    received_messages = defaultdict(list)

    def event_logger(event):
        received_messages[event.modifier_id].append(event)

    received_messages_resource.add_listener(event_logger)
    actuator = Actuator(received_messages_resource)
    environment = Environment(sensors=[], actuators=[actuator])

    root_id = 0
    environment.register_policy(SenderPolicy.__name__, SenderPolicy)
    environment.register_policy(ReceiverPolicy.__name__, ReceiverPolicy)
    ManagerConf = namedtuple('ManagerConf', 'identifier agent_environment')

    try:
        yield ManagerConf(root_id, environment), received_messages, received_messages_resource
    finally:
        environment.unregister_policy(SenderPolicy.__name__)
        environment.unregister_policy(ReceiverPolicy.__name__)


@pytest.mark.asyncio
async def test_interaction_one_direction_sim():
    asyncio.get_event_loop().set_debug(True)
    clock = simulator_clock_factory()
    with sim_environment() as sim_attributes:
        manager_conf, received_messages, received_messages_resource = sim_attributes
        comm_layer = FakeCommunicationLayer()
        agent_manager = SimulatorEnvironmentAgentManager(manager_configuration=manager_conf,
                                                         communication_layer=comm_layer,
                                                         clock=clock)
        await agent_manager.start()

        clock_run_task = asyncio.create_task(clock.run())

        async def wait_for_clock():
            while not clock.started:
                await asyncio.sleep(0)

        await wait_for_clock()

        result = await agent_manager.spawn_agent(policies={SenderPolicy.__name__: 10,
                                                           ReceiverPolicy.__name__: None})
        assert result == 'Agent 0.1 created'
        result = await agent_manager.spawn_agent(policies={SenderPolicy.__name__: 20,
                                                           ReceiverPolicy.__name__: None})
        assert result == 'Agent 0.2 created'

        first_agent = AgentID(0, 1)
        second_agent = AgentID(0, 2)
        await agent_manager.update_agents_relationship(from_agent=first_agent,
                                                       to_agent=str(second_agent),
                                                       operation='add')
        await agent_manager.update_agents_relationship(from_agent=second_agent,
                                                       to_agent=str(first_agent),
                                                       operation='add')

        async def run_for_some_time(upper):
            while clock.epoch_time.epoch < upper:
                await asyncio.sleep(clock.seconds_between_ticks)

        await run_for_some_time(102)

        actuators = await agent_manager.agents_status(request_type=PayloadType.actuators,
                                                      provider=first_agent)

        assert actuators.sender_id == str(first_agent)
        assert actuators.content.touchpoint['ReceivedMessagesResource'] == 15

        actuators = await agent_manager.agents_status(request_type=PayloadType.actuators,
                                                      provider=second_agent)
        assert actuators.sender_id == str(second_agent)
        assert actuators.content.touchpoint['ReceivedMessagesResource'] == 15

        assert received_messages_resource.value == 15
        assert len(received_messages[str(AgentID(0, 2))]) == 10
        assert len(received_messages[str(AgentID(0, 1))]) == 5

        clock_run_task.cancel()
        await clock_run_task

        for agent in agent_manager.running_agents.values():
            remove_logger_files(agent.metrics_logger.logger)


@contextlib.asynccontextmanager
async def real_environment(comm_layer_type):
    ManagerConf = namedtuple('ManagerConf', 'identifier agent_config agents_directory comm_layer_type')
    root_id = 0

    with start_agents_directory() as agents_directory_port:
        agents_directory = {'address': platform.node(), 'port': agents_directory_port}
        conf = pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_agent.conf'
        manager_conf = ManagerConf(root_id, conf, agents_directory, comm_layer_type)

        agent_manager = RealEnvironmentAgentManager(manager_conf, quiet=True)
        await agent_manager.start()

        try:
            yield agent_manager
        except Exception as err:
            pytest.fail(err)

        for agent in agent_manager.running_agents.values():
            remove_process_files(agent.pid)

        await agent_manager.cleanup()


@pytest.mark.parametrize('comm_layer_type', ['raw', 'REST'])
@pytest.mark.asyncio
async def test_interaction_one_direction_real(comm_layer_type):
    logger = logging.getLogger()
    logger_setup.set_to_rotate(logger, level=logging.DEBUG, file_name_prefix='agent_manager_runner')

    async with real_environment(comm_layer_type) as agent_manager:
        start = time.time()

        # Since this is a real environment, periodic actions need to
        # be greater than 2 to guarantee that the results will be
        # deterministic,
        content = await agent_manager.spawn_agent(policies={SenderPolicy.__name__: 1,
                                                            ReceiverPolicy.__name__: None})
        assert content == 'Agent 0.1 created'
        content = await agent_manager.spawn_agent(policies={SenderPolicy.__name__: 2,
                                                            ReceiverPolicy.__name__: None})
        assert content == 'Agent 0.2 created'

        first_agent = AgentID(0, 1)
        second_agent = AgentID(0, 2)
        result = await agent_manager.update_agents_relationship(from_agent=first_agent,
                                                                to_agent=str(second_agent),
                                                                operation='add')
        assert result.content.status == 'Operation include_as_related of 0.2 performed in 0.1'
        result = await agent_manager.update_agents_relationship(from_agent=second_agent,
                                                                to_agent=str(first_agent),
                                                                operation='add')
        assert result.content.status == 'Operation include_as_related of 0.1 performed in 0.2'

        info = await agent_manager.agents_status(request_type=PayloadType.info,
                                                 provider=first_agent)
        assert info.type == PayloadType.info, info.content
        first_related_agents = info.content.related_agents

        info = await agent_manager.agents_status(request_type=PayloadType.info,
                                                 provider=second_agent)
        assert info.type == PayloadType.info, info.content
        second_related_agents = info.content.related_agents

        assert any(i in first_related_agents for i in [str(first_agent),
                                                       str(second_agent)])
        assert any(i in second_related_agents for i in [str(first_agent),
                                                        str(second_agent)])
        assert first_related_agents != second_related_agents

        wait_time = 5
        await asyncio.sleep(wait_time)  # extra time to allow resource modification

        actuators = await agent_manager.agents_status(request_type=PayloadType.actuators,
                                                      provider=first_agent)

        resource_from_first_agent = actuators.content.touchpoint['ReceivedMessagesResource']

        actuators = await agent_manager.agents_status(request_type=PayloadType.actuators,
                                                      provider=second_agent)
        resource_from_second_agent = actuators.content.touchpoint['ReceivedMessagesResource']

        elapsed_time = time.time() - start  # amount time

        # Since the agents are running in the actual environment, it
        # is not possible to assert to a deterministc value.
        # We can guess an interval based on the elapsed time.

        assert resource_from_first_agent < elapsed_time / 3
        assert resource_from_second_agent < elapsed_time
        # First agent executes SenderPolicy every seconds. Second
        # agent executes SenderPolicy every two seconds. This means
        # that first agent will receive no more than twice the message
        # that has second message has received
        assert resource_from_second_agent >= resource_from_first_agent * 2

        remove_logger_files(logger)

if __name__ == '__main__':
    pytest.main([__file__])
