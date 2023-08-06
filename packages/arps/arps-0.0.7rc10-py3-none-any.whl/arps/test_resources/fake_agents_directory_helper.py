import platform

from arps.core.real.rest_api_utils import JSONType
from arps.core.real.agents_directory_helper import AgentsDirectoryHelperError


class FakeAgentsDirectoryHelper:

    def __init__(self):
        self.registered = {}

    def get(self, *, agent_id: str) -> JSONType:
        try:
            return {'address': platform.node(),
                    'port': self.registered[agent_id]}
        except KeyError:
            raise AgentsDirectoryHelperError(f'Agent {agent_id} not found')

    def add(self, *, agent_id: str, address: str, port: int) -> JSONType:
        if agent_id in self.registered and self.registered[agent_id] != str(port):
            message = f'Agent {agent_id} is already added but with different parameters'
            raise AgentsDirectoryHelperError(message)
        self.registered[agent_id] = str(port)
        return f'Agent {agent_id} added'

    def remove(self, *, agent_id: str) -> JSONType:
        try:
            del self.registered[agent_id]
            return f'Agent {agent_id} removed'
        except KeyError:
            raise AgentsDirectoryHelperError(f'Agent {agent_id} not found')

    def list(self) -> JSONType:
        return self.registered

    def about(self) -> JSONType:
        return ''

    def available_commands(self) -> JSONType:
        return {}
