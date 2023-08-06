import asyncio
import pickle

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import Payload, PayloadType, response_factory
from arps.core.real.real_communication_layer import RealCommunicationLayer


class RawCommunicationLayer(RealCommunicationLayer):
    def __init__(self, port: int, agents_directory_helper):
        """Initializes the raw communication layer.

        This layer supports p2p communication using
        Payload serialized as message

        Args:
        - port: port to list the requisitions
        - agents_directory_helper: helper with means to access the
        agents directory service

        """
        self.server = None

        super().__init__(port, agents_directory_helper)

    async def _send(self, message: Payload, agent_src: AgentID, agent_dst: AgentID):
        try:
            address, port = self.agent_endpoint(agent_dst)
        except ValueError as err:
            error_response = response_factory(
                PayloadType.error,
                str(agent_src),
                str(agent_dst),
                message.message_id,
                str(err),
            )
            await self.receive(error_response)
            return

        self.logger.info('accessing %s through %s:%s', agent_dst, address, port)
        _, writer = await asyncio.open_connection(address, int(port))
        content = pickle.dumps(message)
        self.logger.debug('writing %s to agent %s', message, agent_dst)
        writer.write(content)

        writer.write_eof()

        await writer.drain()

    async def start(self):
        self.server = await asyncio.start_server(self.handle_connection, port=self.port)
        self.logger.info('Serving on %s', self.server.sockets[0].getsockname())

    async def close(self):
        self.server.close()
        self.logger.info('waiting server to be closed')
        await self.server.wait_closed()
        self.logger.info('server closed')

    async def handle_connection(self, client_reader, client_writer):
        task = asyncio.create_task(self._handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader, client_writer)

        def client_done(task):
            self.logger.info('client task done: %s', task)
            del self.clients[task]

        task.add_done_callback(client_done)

    async def _handle_client(self, client_reader, client_writer):
        self.logger.info('handling client')
        line = await client_reader.read()
        data = pickle.loads(line)
        self.logger.info('received data request info %s', data)
        self.logger.debug('receive registered %s', self.receive)
        await self.receive(data)
