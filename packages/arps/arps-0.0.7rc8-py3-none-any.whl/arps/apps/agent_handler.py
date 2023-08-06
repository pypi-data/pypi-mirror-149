import logging
from typing import Dict, Optional

from arps.core.agent_factory import AgentCreationError, AgentFactory, build_agent
from arps.core.agent_id_manager import AgentID
from arps.core.clock import Clock
from arps.core.metrics_logger import MetricsLoggers
from arps.core.real.real_communication_layer import RealCommunicationLayer


class AgentHandler:
    """
    This class control the life cycle of an agent.

    By default the agent will be listening the port 8888

    Raises AgentCreationError from build_agent when agent creation fails.
    """

    def __init__(
        self,
        environment,
        clock,
        agent_id,
        agent_port=8888,
        policies=None,
        agents_directory_helper=None,
        comm_layer_cls=None,
    ):
        """Initialize agent handler instance

        Params:
        - environment: agent environment
        - agent_id: instance of AgentID created by AgentIDManager
        - agent_port: listening port (default: 8888)
        - policies: policies that will control the agent behaviour
        - agents_directory_helper: agents discovery service where the
          agent will be registered
        - comm_layer_cls: implementation of RealCommunicationLayer
        """
        assert issubclass(comm_layer_cls, RealCommunicationLayer)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = agent_id
        self.communication_layer = comm_layer_cls(agent_port, agents_directory_helper)

        self.clock = clock
        try:
            agent_factory = AgentFactory(
                environment=environment, communication_layer=self.communication_layer, metrics_loggers=MetricsLoggers()
            )
            self.agent = self.create_agent(agent_factory, agent_id=self.agent_id, policies=policies or {}, clock=clock)
        except AgentCreationError as err:
            self.logger.error(err)
            raise RuntimeError(err)
        self.port = agent_port
        self.logger.info('created agent server %s to listen on %s', self.agent_id, agent_port)

    async def start(self):
        self.logger.info('agent has started')
        await self.communication_layer.start()
        self.clock.add_listener(self.agent.run)

    async def finalize(self):
        self.communication_layer.unregister(self.agent.identifier)
        await self.communication_layer.close()
        self.logger.info('agent has stopped')

    def create_agent(self, agent_factory, agent_id: AgentID, policies: Dict[str, Optional[int]], clock: Clock):
        self.logger.info('Policies: %s', policies)
        agent = build_agent(agent_factory, agent_id, policies, clock)

        return agent
