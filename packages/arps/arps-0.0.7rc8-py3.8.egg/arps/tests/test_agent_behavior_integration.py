import logging
import asyncio

import pytest # type: ignore

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.clock import EpochTime
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.policies_executor import PoliciesExecutor
from arps.core.payload_factory import (Request,
                                       PayloadType)

from arps.core.remove_logger_files import remove_logger_files

from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer


class EchoUserProcess(PoliciesExecutor):

    def __init__(self, **kwargs):
        self.agents_applications = kwargs.pop('agents_applications', None)
        super().__init__(**kwargs, policies=[],
                         epoch_time=EpochTime(),
                         clock_callback=(lambda _: None, lambda _: None))
        self.logger = logging.getLogger('test.echo_process_user')

    async def run(self):
        for agent in self.agents_applications:
            self.logger.info(
                'agent {} sending echo req to agent {}'.format(
                    self.host.identifier, agent))
            request = Request(str(self.host.identifier),
                              str(agent),
                              type=PayloadType.action,
                              message_id=None,
                              content='echo')
            await self.host.send(request, agent_dst=agent)
            self.logger.info(
                'agent {} sent echo req to agent {}'.format(
                    self.host.identifier, agent))


class EchoProviderProcess(PoliciesExecutor):

    def __init__(self, **kwargs):
        self.message = None
        super().__init__(**kwargs, policies=[],
                         epoch_time=EpochTime(),
                         clock_callback=(lambda _: None, lambda _: None))
        self.logger = logging.getLogger('test.echo_process_provider')

    def receive(self, event):
        self.message = event
        self.logger.info('agent received {}'.format(event))


@pytest.fixture()
def setup_environment():
    agent_id_manager = AgentIDManager(0)

    def new_agent_id():
        agent_id = agent_id_manager.next_available_id()
        agent_id_manager.commit()
        return agent_id

    comm_layer = FakeCommunicationLayer()
    asyncio.run(comm_layer.start())
    agent_factory = AgentFactory(metrics_loggers=MetricsLoggers(),
                                 communication_layer=comm_layer,
                                 environment=Environment(sensors=[], actuators=[]))

    return new_agent_id, agent_factory


@pytest.mark.asyncio
async def test_basic_p2p_communication(setup_environment):
    id_generator, agent_factory = setup_environment
    agents_identifier = [id_generator() for _ in range(2)]
    user_process = EchoUserProcess(agents_applications=[agents_identifier[1]])
    provider_process = EchoProviderProcess()

    user_process_agent = agent_factory.create_agent(
        identifier=agents_identifier[0], policies_executor=user_process)

    provider_process_agent = agent_factory.create_agent(
        identifier=agents_identifier[1], policies_executor=provider_process)

    assert provider_process.message is None

    await user_process_agent.run()

    received = Request('0.1', '0.2', PayloadType.action, None, 'echo')
    assert received  == provider_process.message

    remove_logger_files(user_process_agent.metrics_logger.logger)
    remove_logger_files(provider_process_agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_multiple_p2p_communication(setup_environment):
    id_generator, agent_factory = setup_environment

    # There will be three agents, but user 0.1 will communicate only
    # with provider 0.2 and 0.4
    agents_identifier = [id_generator() for _ in range(4)]

    user_process = EchoUserProcess(agents_applications=[agents_identifier[1],
                                                        agents_identifier[3]])

    user_process_agent = agent_factory.create_agent(
        identifier=agents_identifier[0], policies_executor=user_process)

    def create_provider_agent(provider_process_id):
        provider_process_agent = agent_factory.create_agent(
            identifier=provider_process_id, policies_executor=EchoProviderProcess())
        assert provider_process_agent.policies_executor.message is None
        return provider_process_agent

    provider_process_agents = [create_provider_agent(agents_identifier[i]) for i in range(1, 4)]

    await user_process_agent.run()

    received = lambda uid: Request('0.1', uid,
                                   PayloadType.action, None, 'echo')
    assert received('0.2') == provider_process_agents[0].policies_executor.message
    assert provider_process_agents[1].policies_executor.message is None
    assert received('0.4') == provider_process_agents[2].policies_executor.message

    remove_logger_files(user_process_agent.metrics_logger.logger)
    for provider_process_agent in provider_process_agents:
        remove_logger_files(provider_process_agent.metrics_logger.logger)


if __name__ == "__main__":
    pytest.main([__file__])
