import logging
import sys
import argparse
import asyncio
from typing import Any

from arps import __version__ as arps_version
from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (request_factory,
                                       PayloadType,
                                       parse_payload_type)
from arps.core.communication_layer import (CommunicableEntity,
                                           CommunicationLayer)
from arps.core.real.raw_communication_layer import RawCommunicationLayer
from arps.core.real.rest_communication_layer import RESTCommunicationLayer

from arps.core.real.agents_directory_helper import AgentsDirectoryHelper
from arps.core.real.rest_api_utils import random_port


class AgentClient(CommunicableEntity):

    def __init__(self,
                 identifier: AgentID,
                 communication_layer: CommunicationLayer):
        self.comm_layer = communication_layer
        self.messages = dict()
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(identifier=identifier,
                         communication_layer=self.comm_layer)

    async def send_request(self,
                           receiver_id: AgentID,
                           request_type: PayloadType,
                           content: Any = None):

        message = asyncio.Future()
        message_id = id(asyncio.Future())
        self.messages[message_id] = message

        request = request_factory(request_type,
                                  str(self.identifier),
                                  str(receiver_id),
                                  message_id,
                                  content)
        self.logger.info('Request %s created', request)

        try:
            await self.send(request, receiver_id)

            await self.messages[message_id]

            return self.messages[message_id].result()
        finally:
            del self.messages[message_id]

    async def receive(self, message):
        self.logger.info('received data request info %s', message)
        message_id = message.message_id
        self.messages[message_id].set_result(message)
        self.logger.debug('Received messages identifiers: %s', self.messages.keys())
        self.logger.info('Received message: %s', message)

    async def finalize(self):
        self.logger.info('remove agent client from agents directory service')

        self.comm_layer.unregister(self.identifier)


async def run_client():
    logging.basicConfig(filename='agent_client.log', level=logging.INFO)

    parsed_args = parse_arguments()

    content = []
    if parsed_args.request_type == 'policy' and parsed_args.operation and parsed_args.policy:
        content = [parsed_args.operation, parsed_args.policy]

    assert parsed_args.agent
    assert parsed_args.agents_directory

    ad_address, ad_port = parsed_args.agents_directory

    agents_directory_helper = AgentsDirectoryHelper(address=ad_address,
                                                    port=int(ad_port))

    if parsed_args.comm_layer == 'raw':
        comm_layer = RawCommunicationLayer(random_port(), agents_directory_helper)
    elif parsed_args.comm_layer == 'REST':
        comm_layer = RESTCommunicationLayer(random_port(), agents_directory_helper)
    else:
        raise ValueError('Invalid Communication Layer selected. Expect raw or REST')

    await comm_layer.start()

    agent_client = AgentClient(AgentID(parsed_args.id[0], parsed_args.id[1]), comm_layer)

    try:
        return await agent_client.send_request(receiver_id=parsed_args.agent,
                                               request_type=parse_payload_type(parsed_args.request_type),
                                               content=content)
    except (RuntimeError, ValueError) as err:
        return str(err)
    finally:
        await agent_client.finalize()

        await comm_layer.close()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Client that can make requests to agents')
    parser.add_argument('--id', nargs=2, metavar=('manager id', 'agent id'), type=int,
                        help='Manager id and agent id')
    parser.add_argument(
        '--request_type',
        choices=['info', 'sensors', 'actuators', 'policy'],
        help='request type to be sent to agent')
    subparser_policy = parser.add_subparsers(help='policy request arguments')
    parser_policy = subparser_policy.add_parser(
        'policy_args', help='policy arguments')
    parser_policy.add_argument('--policy',
                               default=None,
                               help='policy name')
    parser_policy.add_argument(
        '--operation',
        choices=['add', 'remove'],
        default=None,
        help='policy operation')
    parser.add_argument('--agent',
                        type=str,
                        required=True,
                        help='agent id')
    parser.add_argument('--agents_directory',
                        nargs=2,
                        required=True,
                        metavar=('ADDRESS', 'PORT'),
                        help='agents directory address, and port')
    parser.add_argument('--comm_layer', required=True,
                        choices=['REST', 'raw'],
                        help='Type of communication layer used. Options: REST or raw')
    parser.add_argument('--version', action='version', version=f'ARPS {arps_version}')
    return parser.parse_args()


def main():
    agents_status = asyncio.run(run_client())

    logger = logging.getLogger('AgentClient')
    print(agents_status)
    logger.info('result %s', agents_status)

if __name__ == '__main__':
    main()
    sys.exit(0)
