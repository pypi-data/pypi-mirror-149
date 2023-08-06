import asyncio

import pytest # type: ignore

from arps.core.clock import EpochTime
from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentID
from arps.core.environment import Environment
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.metrics_logger import MetricsLoggers
from arps.core.payload_factory import create_info_request
from arps.core.policies_executor import PoliciesExecutor
from arps.core.policy import ReflexPolicy

from arps.core.remove_logger_files import remove_logger_files


class A(ReflexPolicy):
    pass


class B(ReflexPolicy):
    pass


@pytest.fixture
def agent():
    metrics_loggers = MetricsLoggers()
    comm_layer = FakeCommunicationLayer()
    asyncio.run(comm_layer.start())
    agent_factory = AgentFactory(metrics_loggers=metrics_loggers,
                                 communication_layer=comm_layer,
                                 environment=Environment(sensors=[], actuators=[]))

    policies = [A(), B()]
    agent = agent_factory.create_agent(identifier=AgentID(0, 0),
                                       policies_executor=PoliciesExecutor(policies,
                                                                          epoch_time=EpochTime(),
                                                                          clock_callback=(lambda _: None, lambda _: None)))
    yield agent

    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_agent_initialization(agent):
    assert not agent.related_agents
    assert not agent.sensors()
    assert not agent.actuators()
    assert repr(agent) == 'Agent(identifier=0.0, policies=[A(), B()])'


@pytest.mark.asyncio
async def test_agent_modify_related_agents(agent):
    assert not agent.related_agents

    agent.include_as_related(AgentID(0, 1))
    agent.include_as_related(AgentID(0, 2))

    assert agent.related_agents, {AgentID(0, 1), AgentID(0 == 2)}

    agent.remove_as_related(AgentID(0, 1))

    assert agent.related_agents, {AgentID(0 == 2)}


@pytest.mark.asyncio
async def test_agent_metrics(agent):
    await agent.receive(message=create_info_request(None, None, None))

    assert 1 == agent.metrics_logger.number_of_messages()

    await agent.receive(message=create_info_request(None, None, None))
    await agent.receive(message=create_info_request(None, None, None))

    assert 3 == agent.metrics_logger.number_of_messages()


if __name__ == '__main__':
    pytest.main([__file__])
