import asyncio
import os
import pathlib
import subprocess
from typing import Dict, List, Optional, Type, Union

import psutil  # type: ignore
import simplejson as json

from arps.apps.agent_manager import (
    AgentManager,
    AgentManagerCreationError,
    AgentManagerRequestError,
    JSONType,
)
from arps.apps.client import AgentClient
from arps.apps.multiplatform_process import create_process, terminate_process
from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import PayloadType, parse_payload_type
from arps.core.real.agents_directory_helper import AgentsDirectoryHelper
from arps.core.real.raw_communication_layer import RawCommunicationLayer
from arps.core.real.real_communication_layer import RegistrationError
from arps.core.real.rest_api_utils import random_port
from arps.core.real.rest_communication_layer import RESTCommunicationLayer


class RealEnvironmentAgentManager(AgentManager):
    def __init__(self, manager_configuration, quiet: Optional[bool] = False):
        self.quiet = quiet
        self.comm_layer_type = manager_configuration.comm_layer_type
        comm_layer_cls: Union[Type[RawCommunicationLayer], Type[RESTCommunicationLayer]]
        if self.comm_layer_type == 'raw':
            comm_layer_cls = RawCommunicationLayer
        elif self.comm_layer_type == 'REST':
            comm_layer_cls = RESTCommunicationLayer
        else:
            raise AgentManagerCreationError(
                'Invalid Communication Layer Class. Check configuration file. "comm_layer" options are "raw" or "REST"'
            )

        self.agent_config = manager_configuration.agent_config
        self.agents_directory = manager_configuration.agents_directory
        self.agents_directory_helper = AgentsDirectoryHelper(**self.agents_directory)

        super().__init__(manager_configuration.identifier)

        base_port = random_port()

        self.comm_layer = comm_layer_cls(base_port, self.agents_directory_helper)
        self.agent_client: AgentClient

        self.loaded_policies = self.load_policies_available()

    async def start(self):
        await self.comm_layer.start()
        try:
            client_id = AgentID(self.identifier, 0)
            self.agent_client = AgentClient(
                identifier=client_id, communication_layer=self.comm_layer
            )
        except RegistrationError as err:
            message = f'Error: {err}. \nCheck the identifier field in the configuration file or if there is other agent manager running.'
            message += 'If not remove manually from agents directory. Check if agents directory is running'
            raise AgentManagerCreationError(message)

    async def spawn_agent(self, *, policies: Dict[str, Optional[int]]) -> JSONType:
        if not policies:
            raise AgentManagerRequestError('agent not created, no policy specified')

        agent_id = self.agent_id_manager.next_available_id()
        port = random_port()
        popen = [
            'agent_runner',
            '--id',
            str(agent_id.root_id),
            str(agent_id.agent_identifier),
            '--port',
            str(port),
            '--agents_dir_addr',
            self.agents_directory['address'],
            '--agents_dir_port',
            str(self.agents_directory['port']),
            '--config_file',
            str(self.agent_config),
            '--comm_layer',
            self.comm_layer_type,
        ]

        if self.quiet:
            popen.append('--quiet')
        self.logger.debug('Spawning agents with policies: %s', policies)
        for policy, period in policies.items():
            if period is not None:
                popen.extend(('--periodic_policy', policy, str(period)))
            else:
                popen.extend(('--policy', policy))

        self.logger.debug('Agent paramaters %s', popen)

        (success, message), proc = create_process(
            popen, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        if not success:
            raise AgentManagerRequestError(message)

        self.running_agents[(agent_id, port)] = proc
        self.agent_id_manager.commit()

        return f'Agent {agent_id} created'

    def list_agents(self) -> JSONType:
        running_agents = sorted(str(agent_id) for agent_id, _ in self.running_agents)
        return {'agents': running_agents}

    async def terminate_agent(self, *, agent_id: AgentID) -> JSONType:
        if agent_id not in [agent_id for agent_id, _ in self.running_agents]:
            raise AgentManagerRequestError(
                'Agent id not found. Try list_agents resource to list available agents'
            )

        self.logger.info('Requested termination of agent %s', agent_id)

        agent_proc, port = next(
            (agent_proc, port)
            for (running_agent_id, port), agent_proc in self.running_agents.items()
            if running_agent_id == agent_id
        )

        self.logger.info(
            'Signal sent to agent %s (pid: %s). Waiting until is terminated',
            agent_id,
            agent_proc.pid,
        )
        self.remove_process_files(agent_proc.pid)
        returncode, message = terminate_process(agent_proc)

        self.logger.info('Unregistering Agent %s', (agent_id, port))
        del self.running_agents[(agent_id, port)]

        self.logger.info(
            'Agent %s finalized, return code set as %s', agent_id, returncode
        )
        if returncode != 0:
            self.logger.info(message)
            self.logger.info('Removing agent %s from agents_directory', agent_id)
            # Sometimes the agent fails to terminate correctly but
            # removes itself from the yellow pages
            self.agents_directory_helper.remove(parameters={'id': agent_id})
            return (
                f'Return code is not 0, agent {agent_id} has been forcefully terminated'
            )

        message = f'Agent {agent_id} terminated successfully'

        self.logger.info(message)

        return message

    def remove_process_files(self, pid):
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            self.logger.warning('No such process %s', pid)

        files = [pathlib.Path(pfile.path) for pfile in process.open_files()]
        files = [pfile for pfile in files if pfile.suffix == '.log']
        for f in files:
            try:
                os.remove(f)
            except (PermissionError, FileNotFoundError, OSError) as err:
                self.logger.warning('Error: %s', err)

    async def _agent_status(self, request_type: PayloadType, provider: AgentID):
        try:
            request_type = parse_payload_type(request_type)

            result = await self.agent_client.send_request(provider, request_type)

            self.logger.debug('agent_status returns: %s', result)
            return result
        except ValueError as error:
            message = 'Invalid request type: {}'.format(error)
            self.logger.error(message)
            raise AgentManagerRequestError(message)

    async def update_agents_relationship(
        self, *, from_agent: AgentID, to_agent: str, operation: str
    ):
        content = {'operation': operation, 'to_agent': to_agent}

        result = await self.agent_client.send_request(
            from_agent, PayloadType.meta_agent, content
        )
        if result.type != PayloadType.error:
            return result

        raise AgentManagerRequestError(result.content)

    async def update_policy(
        self, *, agent_id: AgentID, operation: str, policy: str, period: int
    ):
        content = {'operation': operation, 'policy': policy, 'period': period}

        result = await self.agent_client.send_request(
            agent_id, PayloadType.policy, content
        )
        if result.type != PayloadType.error:
            return result

        raise AgentManagerRequestError(result.content)

    def load_policies_available(self):
        try:
            with open(self.agent_config) as agent_conf:
                agent_config = json.load(agent_conf)

                resources = agent_config['resources']
                resources = [resource['class'] for resource in resources]
                monitor_policies = [
                    f'{resource}MonitorPolicy' for resource in resources
                ]

                policies = agent_config['agent_config']['policies']

                return policies + monitor_policies
        except FileNotFoundError:
            self.logger.error('Check if agent config file %s exists', self.agent_config)
            return []

    async def policy_repository(self) -> JSONType:
        return self.loaded_policies

    async def loaded_touchpoints(self) -> JSONType:
        with open(self.agent_config) as agent_conf:
            agent = json.load(agent_conf)
            agent_config = agent['agent_config']
            sensors: List[str] = []
            actuators: List[str] = []
            for resource in agent['resources']:
                sensors.extend(
                    resource['class']
                    for sensor in agent_config['sensors']
                    if resource['class'] == sensor['resource_id']
                )
                actuators.extend(
                    resource['class']
                    for actuator in agent_config['actuators']
                    if resource['class'] == actuator['resource_id']
                )

            return {'sensors': sensors, 'actuators': actuators}

    async def monitor_logs(self) -> List[str]:
        monitor_providers = await self.filter_agents_with_monitor_policy()

        async def monitor_log_path(monitor_provider):
            awaitable_status = self.agents_status(
                request_type=PayloadType.action, provider=monitor_provider
            )
            result = await asyncio.wait_for(awaitable_status, 10.0)
            return result.content.status

        monitor_logs_path = [
            await monitor_log_path(provider) for provider in monitor_providers
        ]
        self.logger.info('Providers monitor logs: %s', monitor_logs_path)

        return monitor_logs_path

    async def filter_agents_with_monitor_policy(self):
        def is_a_monitor_agent(policies):
            return any(policy.endswith('MonitorPolicy') for policy in policies)

        monitor_providers = list()
        for agent in self.list_agents()['agents']:
            awaitable_status = self.agents_status(
                request_type=PayloadType.info, provider=AgentID.from_str(agent)
            )
            result = await asyncio.wait_for(awaitable_status, 10.0)
            self.logger.debug('Info from agent %s: %s', agent, result)
            if is_a_monitor_agent(result.content.policies):
                monitor_providers.append(AgentID.from_str(result.sender_id))

        self.logger.info('Providers monitoring: %s', monitor_providers)
        return monitor_providers

    def finish_all_agents(self):
        self.logger.info(
            'finalizing agents %s', [agent_id for (agent_id, _) in self.running_agents]
        )

        for (agent_id, _), running_agent in self.running_agents.items():
            self.logger.info('terminating for agent %s', agent_id)
            returncode, message = terminate_process(running_agent, timeout=1)
            self.logger.info('Return code %s for agent %s', returncode, running_agent)
            if returncode != 0:
                self.logger.warning(message)
                self.logger.warning('Removing agent %s from agents_directory', agent_id)
                self.agents_directory_helper.remove(agent_id)

            self.logger.info('Agent %s terminated successfully', agent_id)

    async def cleanup(self):
        self.finish_all_agents()

        await self.agent_client.finalize()

        await self.comm_layer.close()

        self.logger.info('cleanup successfully executed')
