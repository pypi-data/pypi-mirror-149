from arps.core.agent_id_manager import AgentID
from arps.core.communication_layer import (CommunicableEntity,
                                           CommunicationLayer)
from arps.core.payload_factory import Payload


class FakeCommunicationLayer(CommunicationLayer):
    '''
    This class creates a kind of bus where entities can communicate.

    The entity is registered automatically when it is created. However, it need to be
    unregistered if the entity is not running anymore.
    '''

    def __init__(self, *args, **kwargs):
        self._entities = None
        super().__init__(*args, **kwargs)

    async def start(self):
        if self._entities is not None:
            return
        self._entities = {}

    async def close(self):
        self.unregister_all()
        self._entities = None

    @property
    def entities(self):
        return self._entities

    def register(self, entity: CommunicableEntity):
        self.logger.info('Trying to register entity %s', entity.identifier)
        if entity.identifier in self.entities.keys():
            self.logger.warning(
                'Entity registration failed. Current entities in the system %s',
                self.entities.keys(),
            )
            raise RuntimeError(
                'Entity {} already in the environment'.format(entity.identifier)
            )

        self.logger.debug('Entity %s registered successfully', entity.identifier)
        self.entities[entity.identifier] = entity

    def unregister(self, entity_identifier: AgentID):
        del self.entities[entity_identifier]
        self.logger.info('Entity %s unregistered', entity_identifier)

    def unregister_all(self):
        self.entities.clear()

    def _entities_id(self):
        return self._entities.keys()

    async def _send(self, message: Payload, agent_src: AgentID, agent_dst: AgentID):
        try:
            entity = self._entities[agent_dst]
            self.logger.debug(
                'entity %s sending message to entity %s', agent_src, entity.identifier
            )
            await entity.receive(message)
        except KeyError:
            self.logger.error(
                'sending message %s from %r to %r failed', message, agent_src, agent_dst
            )
            self.logger.error(
                'check if agent %s is registered or if id has the AgentID type. Type of agent id: %s',
                agent_dst,
                type(agent_dst).__name__,
            )
            self.logger.error('Agents available: %s', self._entities.keys())
