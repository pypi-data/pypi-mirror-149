import logging
import abc
from functools import wraps
from typing import Dict, List, Optional

from arps.core.agent_id_manager import AgentIDManager, AgentID
from arps.core.payload_factory import PayloadType
from arps.core.real.rest_api_utils import JSONType


_AVAILABLE_COMMANDS = {}


def _register_command(command_description):
    def _inner_regiser_command(command):
        '''Register function and first line of docstring to be listed as
        available command

        '''

        _AVAILABLE_COMMANDS[command.__name__] = command_description

        @wraps(command)
        def inner(*args, **kwargs):
            return command(*args, **kwargs)
        return inner
    return _inner_regiser_command


class AgentManagerCreationError(Exception):
    '''This exception class is to capture any error related to the
    process of creating an Agent Manager

    '''


class AgentManagerRequestError(Exception):
    '''This exception class is to capture any error related to a
    AgentManager method call

    '''


class AgentManager(metaclass=abc.ABCMeta):
    '''Class responsible for manage agents.

    Coroutines here need to be used using an event loop.

    See integration tests for examples.

    '''

    def __init__(self, identifier):
        self.running_agents = {}
        self.identifier = identifier
        self.agent_id_manager = AgentIDManager(self.identifier)
        self.message_id = 0

        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def index() -> JSONType:
        return {'available_commands': _AVAILABLE_COMMANDS}

    @_register_command('Spawn agent according to the specified policies')
    @abc.abstractmethod
    async def spawn_agent(self, *, policies: Dict[str, Optional[int]]) -> JSONType:
        '''Creates an agent assinging to it the next unique ID

        Keyword args:
        - policies: dictionary of policies and their periods (when
          required)

        Returns:
        - Message about agent creation status

        Raises:
        - AgentManagerRequestError when request has problems and agent
          couldn't be created

        '''

    @_register_command('List spawned agents')
    @abc.abstractmethod
    def list_agents(self) -> JSONType:
        '''
        List all the spawned agents ids
        '''

    @_register_command('Terminate agent manager')
    @abc.abstractmethod
    async def terminate_agent(self, *, agent_id: AgentID) -> JSONType:
        '''Remove the agent from the system. Its ID will be lost and will not be reused

        Param:
        - agent_id: unique agent id

        '''

    @_register_command('Add or remove relationship between agent')
    @abc.abstractmethod
    async def update_agents_relationship(self, *, from_agent: AgentID,
                                         to_agent: str,
                                         operation: str):
        '''Update agents relationship by create or removing the link
        between agents.

        It is unidirectional. If A has a relationship with B and B has
        a relationship with A, removing parenting from A to B will not
        remove pareting from B to A

        Keyword args:
        - from_agent: agent that will be able to send a message to the
          other agent
        - to_agent: agent that will be able to receive a message from
          the other agent
        - operation: add or remove agent relationship
        '''

    @_register_command('Add policy to agent or remove policy from agent')
    @abc.abstractmethod
    async def update_policy(self, *, agent_id: AgentID, operation: str, policy: str, period: int):
        '''Update an agent regarding its policies

        Keyword args:
        - agent_id: agent that will have its policy updated
        - operator: add or remove policy
        - policy: the name of the policy
        - period: mandatory when adding a periodic policy to the agent
        '''

    @_register_command('Return info about the agent or the state of its monitored resources')
    async def agents_status(self,
                            request_type: PayloadType,
                            provider: AgentID) -> JSONType:
        '''Return the current status of agents

        Keyword args:
        - request_type: info, sensors, or actuators
        - provider: agent that will respond the request

        '''
        agents = self.list_agents()['agents']
        if not agents:
            self.logger.info('No agent is running')
            raise AgentManagerRequestError('No agent is running')

        if str(provider) not in agents:
            self.logger.info('Agent %s not found in %s', provider, agents)
            raise AgentManagerRequestError(f'Agent {provider} not found')

        return await self._agent_status(request_type, provider)

    @abc.abstractmethod
    async def _agent_status(self,
                            request_type: PayloadType,
                            provider: AgentID) -> JSONType:
        '''Return the status of the provider based on the request type

        '''

    def generate_message_id(self):
        self.message_id += 1
        return self.message_id

    @_register_command('Show available policies (local and remote)')
    @abc.abstractmethod
    async def policy_repository(self) -> JSONType:
        '''List available policies in the repository used to set agents' behaviour

        '''

    @_register_command('Show available touchpoints')
    @abc.abstractmethod
    async def loaded_touchpoints(self) -> JSONType:
        '''Returns loaded sensors and actuators

        '''

    @_register_command('Retrieve monitor log')
    async def monitor_logs(self) -> List[str]:
        '''Return path to the monitor logs containing states of the touchpoints

        '''

    @abc.abstractmethod
    def cleanup(self):
        '''Stop all agents that was created by the manager.

        Doesn't reset the identifiers.

        '''
