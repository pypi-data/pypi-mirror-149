from functools import wraps, singledispatch
from typing import TypeVar, Optional, Dict, List
from contextlib import suppress

from arps.core.clock import Clock
from arps.core.agent_factory import (AgentFactory, build_agent,
                                     AgentCreationError)
from arps.core.agent_id_manager import AgentID
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.metrics_logger import MetricsLoggers
from arps.core.payload_factory import PayloadType
from arps.core.policies.monitor import MonitorPolicy
from arps.apps.agent_manager import (AgentManager,
                                     JSONType,
                                     AgentManagerRequestError)
from arps.apps.client import AgentClient


class SimulatorEnvironmentAgentManager(AgentManager):

    def __init__(self, *,
                 manager_configuration: TypeVar('SimulatorManagerEnvironment'),
                 communication_layer: FakeCommunicationLayer,
                 clock: Clock):
        self.environment = manager_configuration.agent_environment
        self.communication_layer = communication_layer

        self.metrics_loggers = MetricsLoggers()
        self.agent_factory = AgentFactory(environment=self.environment,
                                          communication_layer=self.communication_layer,
                                          metrics_loggers=self.metrics_loggers)

        self.clock = clock

        super().__init__(manager_configuration.identifier)
        self.client_id = AgentID(self.identifier, 0)
        self.agent_client: AgentClient = None

        self.actions_tracker = list()
        self.agents_monitoring_resources = list()

    async def start(self):
        await self.communication_layer.start()

        self.agent_client = AgentClient(self.client_id, self.communication_layer)

    def tracked_action(method):
        @singledispatch
        def format_action_parameters(param):
            return str(param)

        @format_action_parameters.register
        def _(param: list):
            return [str(value) for value in param]

        @format_action_parameters.register
        def _(param: dict):
            return {str(key): str(value) for key, value in param.items()}

        @wraps(method)
        async def inner(_self, **kwargs):
            action_params = [(k, format_action_parameters(v)) for k, v in kwargs.items()]
            _self.actions_tracker.append((method.__name__, action_params))
            return await method(_self, **kwargs)

        return inner

    @tracked_action
    async def spawn_agent(self, *, policies: Dict[str, Optional[int]]) -> JSONType:
        try:
            if not policies:
                raise AgentManagerRequestError('agent not created, no policy specified')

            self.logger.info('spawn agent with policies %s', policies)

            try:
                agent = self._agent_factory(policies)
            except AgentCreationError as agent_creation_error:
                self.logger.warning(agent_creation_error)
                raise AgentManagerRequestError(str(agent_creation_error))

            self.logger.info('agent %s created at epoch %s', agent.identifier,
                             self.clock.epoch_time.epoch)

            if any(policy for policy in policies if policy.endswith('MonitorPolicy')):
                self.agents_monitoring_resources.append(agent)
            self._add_agent(agent)

            return f'{agent} created'
        except ValueError as error:
            message = 'Invalid input {}'.format(error)
            self.logger.error(message)
            raise AgentManagerRequestError(message)

    def _agent_factory(self, policies):
        agent_id = self.agent_id_manager.next_available_id()

        agent = build_agent(self.agent_factory, agent_id, policies, self.clock)

        self.agent_id_manager.commit()

        return agent

    def list_agents(self) -> JSONType:
        running_agents = sorted(str(agent_id) for agent_id in self.running_agents)
        return {'agents': running_agents}

    @tracked_action
    async def terminate_agent(self, *, agent_id: AgentID) -> JSONType:
        if agent_id not in self.running_agents:
            raise AgentManagerRequestError('Agent id not found. Try list_agents resource to list available agents')

        agent = self.running_agents[agent_id]
        self._remove_agent(agent)
        with suppress(ValueError):
            # if exception is raised, agent is not in the list of
            # agents that are monitoring any resource
            del self.agents_monitoring_resources[self.agents_monitoring_resources.index(agent)]

        return f'Agent {agent_id} terminated successfully'

    async def _agent_status(self, request_type: PayloadType, provider: AgentID):
        try:
            if not self.clock.started:
                error = 'epoch not running, start it by running the simulator before invoking this command'
                self.logger.warning(error)
                raise AgentManagerRequestError(error)

            return await self.agent_client.send_request(provider, request_type)

        except AgentManagerRequestError:
            raise
        except AgentCreationError as error:
            self.logger.error(error)
            raise AgentManagerRequestError(error.msg)
        except ValueError as error:
            message = 'Invalid request type {}'.format(error)
            self.logger.error(message)
            raise AgentManagerRequestError(message)
        except Exception as error:
            message = 'Unknown Error: {}'.format(str(error))
            self.logger.error(message)
            raise AgentManagerRequestError(message)

    async def policy_repository(self) -> JSONType:
        return self.environment.list_registered_policies()

    async def loaded_touchpoints(self) -> JSONType:
        sensors = list(self.environment.sensors.keys())
        actuators = list(self.environment.actuators.keys())

        return {'sensors': sensors, 'actuators': actuators}

    def _add_agent(self, agent):
        self.logger.info('scheduling agent %s', agent.identifier)
        self.clock.add_listener_low_priority(agent.run)
        self.running_agents[agent.identifier] = agent

    def _remove_agent(self, agent):
        self.logger.info('removing agent %s', agent.identifier)
        self.clock.remove_listener(agent.run)
        del self.running_agents[agent.identifier]
        self.communication_layer.unregister(agent.identifier)

    @tracked_action
    async def update_agents_relationship(self, *,
                                         from_agent: AgentID,
                                         to_agent: str,
                                         operation: str):
        if not self.clock.started:
            error = 'epoch not running, start it by running the simulator before invoking this command'
            self.logger.warning(error)
            return AgentManagerRequestError(error)

        content = {'operation': operation, 'to_agent': to_agent}
        result = await self.agent_client.send_request(from_agent,
                                                      PayloadType.meta_agent,
                                                      content)
        if result.type != PayloadType.error:
            return result

        raise AgentManagerRequestError(result.content)


    @tracked_action
    async def update_policy(self, *, agent_id: AgentID,
                            operation: str, policy: str, period: int):
        if not self.clock.started:
            error = 'epoch not running, start it by running the simulator before invoking this command'
            self.logger.warning(error)
            return AgentManagerRequestError(error)
        content = {'operation': operation, 'policy': policy, 'period': period}

        result = await self.agent_client.send_request(agent_id,
                                                      PayloadType.policy,
                                                      content)
        if result.type != PayloadType.error:
            return result

        raise AgentManagerRequestError(result.content)

    async def monitor_logs(self) -> List[str]:
        monitor_logs_path = []
        for agent in self.agents_monitoring_resources:
            for policy in agent.policies_executor._policies:
                if isinstance(policy, MonitorPolicy):
                    monitor_logs_path.append(policy.monitor_logger_path)

        self.logger.info('Providers monitor logs: %s', monitor_logs_path)

        return monitor_logs_path

    def finish_all_agents(self):
        self.communication_layer.unregister_all()

    async def cleanup(self):
        self.finish_all_agents()
