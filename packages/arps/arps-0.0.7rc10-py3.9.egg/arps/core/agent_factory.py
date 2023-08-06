from contextlib import suppress
from typing import Dict, Optional

from arps.core.agent import _AgentImplementation
from arps.core.agent_id_manager import AgentID
from arps.core.clock import Clock
from arps.core.communication_layer import CommunicationLayer
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.policies.info import InfoProviderPolicy
from arps.core.policies.meta import MetaPolicyProvider
from arps.core.policies.meta_agent import MetaAgentProviderPolicy
from arps.core.policies.touchpoint_status import TouchPointStatusProviderPolicy
from arps.core.policies_executor import PoliciesExecutor


class AgentCreationError(Exception):
    """Error raised when agent creation fails"""


class AgentFactory:
    def __init__(
        self,
        *,
        metrics_loggers: MetricsLoggers,
        communication_layer: CommunicationLayer,
        environment: Environment
    ):
        """Creates a new agent factory

        Keyword parameters:

        - metrics_logger: log activities such as number of messages
          exchanged, policies executed, etc.

        - communication_layer : specialization of communication_layer
          class

        - environment : Environment instance with sensors/actuators
        """

        self._metrics_loggers = metrics_loggers

        assert communication_layer, 'Expect an instance of communication layer'
        self._communication_layer = communication_layer
        self.environment = environment

    def create_agent(self, *, identifier, policies_executor: PoliciesExecutor):
        """
        This function creates an agent

        Keyword parameters:
        - identifier: unique id
        - policies: policies executor instance
        """

        metrics_logger = self._metrics_loggers.register(identifier)

        try:
            agent = _AgentImplementation(
                agent_id=identifier,
                communication_layer=self._communication_layer,
                environment=self.environment,
                metrics_logger=metrics_logger,
            )
            agent._add_policies_executor(policies_executor)
        except RuntimeError as error:
            raise AgentCreationError(str(error))

        return agent


def build_agent(
    agent_factory: AgentFactory,
    agent_id: AgentID,
    policies: Dict[str, Optional[int]],
    clock: Clock,
):
    """
    Build an agent according to its factory.

    Agent will have as default policy: InfoProviderPolicy, TouchPointStatusProviderPolicy,
                                       MetaPolicyProvider, MetaAgentProviderPolicy

    Raises AgentCreationError if preconditions for creation is not fulfilled
    """
    try:
        load_policy = agent_factory.environment.load_policy
        user_policies = [load_policy(*item) for item in sorted(policies.items())]
    except ValueError as error:
        raise AgentCreationError(error)

    default_policies = [
        InfoProviderPolicy(),
        TouchPointStatusProviderPolicy(),
        MetaPolicyProvider(),
        MetaAgentProviderPolicy(),
    ]

    all_policies = default_policies + user_policies

    policies_executor = PoliciesExecutor(
        all_policies, clock.epoch_time, clock.observer_interface
    )

    agent = agent_factory.create_agent(
        identifier=agent_id, policies_executor=policies_executor
    )

    for user_policy in user_policies:
        with suppress(AttributeError):
            for required_metric in user_policy.required_metrics:
                agent.metrics_logger.add(required_metric)

    return agent
