from __future__ import annotations

import abc
import logging

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import Payload, PayloadType, create_error_response


class CommunicableEntity(metaclass=abc.ABCMeta):
    def __init__(self, identifier: AgentID, communication_layer: CommunicationLayer):
        """Initializes entity and do the registration of itself in the
        network

        Args:
        - identifier: unique identifier of the entity
        - communication_layer: layer used to communicate with other
        agents
        """
        self.identifier = identifier
        self.communication_layer = communication_layer
        self.communication_layer.register(self)

    async def send(self, message: Payload, agent_dst: AgentID):
        await self.communication_layer.send(message, self.identifier, agent_dst)

    @abc.abstractmethod
    async def receive(self, message: Payload) -> None:
        """Receives a message and process it accordingly with each entity"""


class CommunicationLayer(metaclass=abc.ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def register(self, entity: CommunicableEntity):
        """Register entity to be able to communicate with other entities

        Args:
        - entity: instance of derived class of CommunicableEntity

        """

    @abc.abstractmethod
    def unregister(self, entity: AgentID):
        """Unregister the entity

        Args:
        - entity: instance of derived class of CommunicableEntity

        """

    @abc.abstractmethod
    async def start(self):
        """Prepare layer to start to receive requests"""

    async def send(self, message: Payload, agent_src: AgentID, agent_dst: AgentID):
        """Send message from one agent to another

        Args:
        - message: message to be sent
        - agent_src: agent identifier of the sender
        - agent_dst: agent identifier of the receiver

        """
        if message.type == PayloadType.periodic_action:
            error_rsp = create_error_response(
                str(agent_dst),
                str(agent_src),
                message.message_id,
                'payload type not supported',
            )
            await self.receive(error_rsp)
            return

        await self._send(message, agent_src, agent_dst)

    @abc.abstractmethod
    async def _send(self, message: Payload, agent_src: AgentID, agent_dst: AgentID):
        """The send method is dependent on the derived class. It can use http,
        rpc, or files, for example

        """

    async def receive(self, message: Payload) -> None:
        """What to do with the message received is dependent on the
        implementation of derived classes

        """
        raise NotImplementedError
