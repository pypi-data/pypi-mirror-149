import platform
from typing import Any, Callable, Coroutine, Dict, Tuple

from arps.core.agent_id_manager import AgentID
from arps.core.communication_layer import CommunicableEntity, CommunicationLayer
from arps.core.payload_factory import Payload
from arps.core.real.agents_directory_helper import (
    AgentsDirectoryHelper,
    AgentsDirectoryHelperError,
)


class RegistrationError(Exception):
    """This exception is raised when a failure occur during the entity registration"""


ReceiveCoroutineType = Callable[[Payload], Coroutine[Any, Any, None]]


class RealCommunicationLayer(CommunicationLayer):
    def __init__(self, port: int, agents_directory_helper: AgentsDirectoryHelper):
        """Initializes the communication layer

        Args:
        - port: port to list the requisitions
        - agents_directory_helper: helper with means to access the
        agents directory service

        """

        self.port = port
        self.agents_directory_helper = agents_directory_helper

        # The clients are dependent on the implementation
        self.clients: Dict[Any, Any] = {}
        self._receive: ReceiveCoroutineType

        super().__init__()

    async def receive(self, message: Payload) -> None:
        await self._receive(message)

    def register(self, entity: CommunicableEntity) -> None:
        """Register the agent in the network to be discoverable

        Args:
        - entity: instance of the discoverable entity
        """

        self._receive = entity.receive

        try:
            result = self.agents_directory_helper.add(
                agent_id=str(entity.identifier), address=platform.node(), port=self.port
            )
        except AgentsDirectoryHelperError as err:
            raise RegistrationError(err)

        assert result == f'Agent {entity.identifier} added', result

    def unregister(self, entity_identifier: AgentID) -> None:
        """Remove the agent from the network

        Args:
        - agent_dst: AgentID of the agent to removed from the network
        """
        try:
            self.agents_directory_helper.remove(agent_id=str(entity_identifier))
        except AgentsDirectoryHelperError as err:
            self.logger.warning(str(err))
            raise ValueError(str(err))

    def agent_endpoint(self, agent_dst: AgentID) -> Tuple[str, str]:
        """Finds the agent address and port based on its ID

        Args:
        - agent_dst: AgentID of the agent to be discovered

        Raises:
        - AgentsDirectoryHelperError: when the discovery service is not available
        - ValueError: when the discovery service don't find the agent

        Returns:
        - a tuple containing address and port of the agent, respectively

        """
        try:
            result = self.agents_directory_helper.get(agent_id=str(agent_dst))
        except AgentsDirectoryHelperError as err:
            self.logger.warning(str(err))
            raise ValueError(str(err))
        else:
            # Typing errors below are being ignored since result is a
            # JSONType (an Union of several types)
            #
            # Dict has __getitem__(self, str) but List, str, and int
            # doesn't, so it will complain about this

            address = result['address']  # type: ignore
            port = result['port']  # type: ignore

            return address, port
