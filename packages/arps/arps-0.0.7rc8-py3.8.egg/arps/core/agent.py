import logging
from abc import abstractmethod
from typing import Any, List, Optional, Set

from arps.core.agent_id_manager import AgentID
from arps.core.communication_layer import CommunicableEntity, CommunicationLayer
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.mobile_entity import MobileEntity
from arps.core.payload_factory import Payload
from arps.core.policies_executor import PoliciesExecutor


class Agent(CommunicableEntity, MobileEntity):
    """
    Base class for agents

    An agent has two list of touchpoints available: sensors and actuators
    """

    def __init__(
        self,
        agent_id: AgentID,
        communication_layer: CommunicationLayer,
        environment: Environment,
    ):
        """Initializes the agent

        Params:
        - agent_id: global unique id
        - communication_layer: instance of CommunicationLayer class
        - environment: instance of Environment class
        """

        self._environment = environment
        # Sometimes the related agent can be terminated or be non
        # existent from the beginning.  The decision about what to do
        # when the agent is not found is responsibility of the user. A
        # policy that does not found the agent can simply remove it
        # from this list or it can wait a bit
        self._related_agents: Set[AgentID] = set()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._policies_executor: PoliciesExecutor

        CommunicableEntity.__init__(self, agent_id, communication_layer)
        MobileEntity.__init__(self, self._environment.boundaries)

        assert isinstance(self.identifier, AgentID)

    def include_as_related(self, agent_id: AgentID):
        assert isinstance(agent_id, AgentID)

        self._related_agents.add(agent_id)

    def remove_as_related(self, agent_id: AgentID):
        assert isinstance(agent_id, AgentID)

        self._related_agents.remove(agent_id)

    @property
    def related_agents(self):
        return frozenset(self._related_agents)

    def sensors(self) -> List[str]:
        """
        Returns a list of available sensors
        """
        return list(self._environment.sensors.keys())

    def actuators(self) -> List[str]:
        """
        Returns a list of available actuators
        """
        return list(self._environment.actuators.keys())

    def read_sensor(self, sensor_id: str) -> Any:
        return self._environment.sensors[sensor_id].read()

    def read_actuator(self, actuator_id: str) -> Any:
        return self._environment.actuators[actuator_id].read()

    def modify_actuator(self, actuator_category, **actuator_attributes) -> None:
        return self._environment.actuators[actuator_category].set(**actuator_attributes)

    def add_policy(self, policy_identifier: str, period: Optional[int] = None):
        policy = self._environment.load_policy(policy_identifier, period)
        self._policies_executor.add_policy(policy)

    def is_policy_registered(self, policy_identifier: str) -> bool:
        return self._environment.is_policy_registered(policy_identifier)

    @abstractmethod
    async def run(self):
        """Execute control loop"""


class _AgentImplementation(Agent):
    """Responsible to run process.

    created by agent_factory.create_agent.

    When created a single policies executor is added. This executor
    will take care of the upper layer logic while this class will
    handle host logic.

    """

    def __init__(
        self,
        agent_id: AgentID,
        communication_layer: CommunicationLayer,
        environment: Environment,
        metrics_logger: MetricsLoggers,
    ):
        self._policies_executor: PoliciesExecutor
        self._metrics_logger: MetricsLoggers = metrics_logger
        super().__init__(agent_id, communication_layer, environment)

    @property
    def policies_executor(self):
        return self._policies_executor

    async def receive(self, message: Payload):
        self.logger.debug('agent %s received message ', self.identifier)
        self._policies_executor.receive(message)
        self._metrics_logger.update_number_of_messages()  # type: ignore

    @property
    def metrics_logger(self):
        return self._metrics_logger

    async def run(self):
        self.logger.debug('running agent %s', self.identifier)
        await self._policies_executor.run()

    def _add_policies_executor(self, policies_executor):
        policies_executor.host = self
        self._policies_executor = policies_executor
        logger_name = f'Agent_{self.identifier}_PoliciesExecutor'
        self._policies_executor.logger = logging.getLogger(logger_name)

    def __repr__(self):
        return f'Agent(identifier={self.identifier}, policies={self._policies_executor!r})'

    def __str__(self):
        return 'Agent {}'.format(self.identifier)
