'''This test uses a FakeCommunicationLayer instance since it would be
silly to implement something here to test the interface that all the
other ones (including the ones that uses the real network) are
expected to use the same workflow

'''

import pytest  # type: ignore
import pytest_asyncio

from arps.core.communication_layer import CommunicableEntity
from arps.core.payload_factory import create_action_request
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer


def build_message(*, sender_id, receiver_id, content):
    return create_action_request(sender_id, receiver_id, content)


class Entity(CommunicableEntity):
    def __init__(self, identifier, communication_layer):
        super().__init__(identifier, communication_layer)
        self.message_received = list()

    async def receive(self, message):
        assert self.identifier == message.receiver_id
        self.message_received.append(
            'message \'{}\' from agent {} to agent {}'.format(
                message.content.action, message.sender_id, message.receiver_id
            )
        )

        if 'echo' == message.content.action:
            await self.send(
                build_message(sender_id=message.receiver_id, receiver_id=message.sender_id, content='echo_rcv'),
                message.sender_id,
            )


@pytest_asyncio.fixture
async def communication_layer():
    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()
    yield comm_layer


@pytest.mark.asyncio
async def test_entities_uniquiness(communication_layer):
    IDENTIFIER = 1
    Entity(identifier=IDENTIFIER, communication_layer=communication_layer)
    with pytest.raises(RuntimeError):
        Entity(identifier=IDENTIFIER, communication_layer=communication_layer)


@pytest.mark.asyncio
async def test_p2p_transport_layer(communication_layer):
    entity_one = Entity(identifier=1, communication_layer=communication_layer)
    entity_two = Entity(identifier=2, communication_layer=communication_layer)

    assert not entity_one.message_received
    assert not entity_two.message_received

    await entity_one.send(
        build_message(sender_id=entity_one.identifier, receiver_id=entity_two.identifier, content='echo'),
        entity_two.identifier,
    )

    assert 'message \'echo\' from agent 1 to agent 2' == entity_two.message_received[0]
    assert 'message \'echo_rcv\' from agent 2 to agent 1' == entity_one.message_received[0]


@pytest.mark.asyncio
async def test_entity_lifetime(communication_layer):
    entity = Entity(identifier=1, communication_layer=communication_layer)

    assert 1 in communication_layer.entities.keys()

    communication_layer.unregister(entity.identifier)

    assert 1 not in communication_layer.entities.keys()


@pytest.mark.asyncio
async def test_entities_unregister_all(communication_layer):

    Entity(identifier=1, communication_layer=communication_layer)

    Entity(identifier=2, communication_layer=communication_layer)

    assert 1 in communication_layer.entities.keys()
    assert 2 in communication_layer.entities.keys()

    communication_layer.unregister_all()

    assert 1 not in communication_layer.entities.keys()
    assert 2 not in communication_layer.entities.keys()


if __name__ == "__main__":
    pytest.main([__file__])
