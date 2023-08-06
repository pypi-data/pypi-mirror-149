import asyncio
import platform
import re
from dataclasses import asdict

import simplejson as json
from aiohttp import web  # type: ignore

from arps import __version__ as arps_version
from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (Payload, PayloadType, Request, Response,
                                       parse_payload_type, request_factory,
                                       response_factory)
from arps.core.real.real_communication_layer import RealCommunicationLayer
from arps.core.real.rest_api_utils import (HTTPMethods, async_invoke_rest_ws,
                                           build_http_body_and_header,
                                           build_url)

# I doubt that there will be almost a
# million managers (if it's created
# sequentially) with almost a million
# agents
NON_ARPS_ID = '999999.999999'


class RESTCommunicationLayer(RealCommunicationLayer):
    def __init__(self, port, agents_directory_helper):
        '''Initializes the RESTful communication layer.

        Args:
        - port: port to list the requisitions
        - agents_directory_helper: helper with means to access the
        agents directory service

        '''
        self.webapp_runner = None

        # The RealCommunicationLayer is
        # not shared like the
        # FakeCommunicationLayer, so no
        # problem in having the id here
        # as well
        self.host_identifier = None
        self.resources = tuple(
            p.name
            for p in PayloadType
            if p not in [PayloadType.error, PayloadType.periodic_action]
        )
        self.resources_available = {
            'resources_available': ['/' + r for r in self.resources]
        }
        super().__init__(port, agents_directory_helper)

    def register(self, entity):
        self.host_identifier = entity.identifier
        super().register(entity)

    async def _send(self, message: Payload, agent_src: AgentID, agent_dst: AgentID):
        if isinstance(message, Request):
            await self.send_request(message, agent_src, agent_dst)
        elif isinstance(message, Response):
            await self.send_response(message, agent_src, agent_dst)
        else:
            self.logger.error(
                'Message has type %s. Only Request and Response', type(message)
            )

    async def send_request(self, message, agent_src, agent_dst):
        self.logger.debug('Sending a message of type REQUEST')
        try:
            address, port = self.agent_endpoint(agent_dst)
        except ValueError as err:
            error_response = response_factory(
                PayloadType.error, agent_src, agent_dst, message.message_id, str(err)
            )
            await self.receive(error_response)
            return

        body = {}
        method = HTTPMethods.GET
        if message.type in (
            PayloadType.policy,
            PayloadType.meta_agent,
            PayloadType.action,
        ):
            method = HTTPMethods.PUT
        if message.type == PayloadType.policy:
            body = {'op': message.content.op.name, **message.content.meta}
        elif message.type == PayloadType.meta_agent:
            body = {'op': message.content.op.name, 'agent': message.content.meta}

        url = build_url(f'{address}:{port}', message.type.name)

        headers = {'User-Agent': f'ARPSAgent/{arps_version} (requester {agent_src})'}
        body, headers = build_http_body_and_header(body=body, headers=headers)
        self.logger.info(
            'Accessing resource %s with body %s and headers %s', url, body, headers
        )

        content, status = await async_invoke_rest_ws(method, url, body, headers)

        if status.code > 400:
            error_response = response_factory(
                PayloadType.error,
                agent_src,
                agent_dst,
                message.message_id,
                status.reason,
            )
            await self.receive(error_response)
            return

        if content['type'] == PayloadType.info:
            content['content'] = content['content'].values()
        elif content['type'] in [PayloadType.sensors, PayloadType.actuators]:
            content['content'] = content['content']['touchpoint']
        elif content['type'] in [
            PayloadType.policy,
            PayloadType.meta_agent,
            PayloadType.action,
        ]:
            content['content'] = content['content']['status']

        response = response_factory(
            parse_payload_type(content['type']),
            content['sender_id'],
            content['receiver_id'],
            message.message_id,
            content['content'],
        )
        self.logger.info('Received %s from %s', response, url)
        await self.receive(response)

    async def send_response(self, message, agent_src, agent_dst):
        self.logger.debug('creating send response %s', message)
        message_id = message.message_id
        self.clients[message_id].set_result(message)

    def generate_client_id(self, headers):
        agent_id = NON_ARPS_ID
        if 'User-Agent' in headers:
            user_agents = headers['User-Agent']
            self.logger.debug('User agent %s', user_agents)
            user_agent_info = re.search(r'(.*)/.* \(.* (.*)\)', user_agents)
            if user_agent_info and user_agent_info.group(1) == 'ARPSAgent':
                return user_agent_info.group(2)
        self.logger.debug('Client id %s', agent_id)
        return agent_id

    # Resources

    async def request(self, request):
        request_type = request.match_info['request_type']
        self.logger.debug('Received request of type %s', request_type)

        if request_type not in self.resources:
            error_message = f'Unsupported request type: {request_type}. '
            error_message += 'Access / to see list of available resource'
            raise web.HTTPBadRequest(reason=error_message)

        try:
            payload_type = parse_payload_type(request_type)
        except ValueError as error:
            raise web.HTTPBadRequest(reason=error)

        message = asyncio.Future()
        message_id = id(message)
        self.clients[message_id] = message

        agent_id = self.generate_client_id(request.headers)

        content = None
        if request.method == 'PUT':
            content = await self.build_content(request, payload_type)

        await self.receive(
            request_factory(
                payload_type, agent_id, str(self.host_identifier), message_id, content
            )
        )

        try:
            await asyncio.wait_for(message, timeout=10)

            result = asdict(message.result())

            if agent_id == NON_ARPS_ID:
                # since it doesn't matter for non ARPS requesters
                del result['receiver_id']

            return web.json_response(data=result)
        except asyncio.TimeoutError:
            error_message = f'Timeout. Unable to fulfill {payload_type.name} request'
            self.logger.error(error_message)
            raise web.HTTPGatewayTimeout(reason=error_message)
        finally:
            del self.clients[message_id]

    async def build_content(self, request, payload_type):
        if not request.can_read_body:
            message = 'Body is expected to perform the operation'
            raise web.HTTPBadRequest(reason=message)

        content = await request.content.read()
        content = json.loads(content.decode())

        if payload_type == PayloadType.policy:
            content = {
                'operation': content['op'],
                'policy': content['policy'],
                'period': content.get('period'),
            }
        elif payload_type == PayloadType.meta_agent:
            content = {'operation': content['op'], 'to_agent': content['agent']}
        self.logger.debug('content %s', content)

        return content

    async def index(self, request):
        return web.json_response(data=self.resources_available)

    async def start(self):
        app = web.Application()
        app.add_routes(
            [
                web.get('/{request_type}', self.request),
                web.put('/{request_type}', self.request),
                web.get('/', self.index),
            ]
        )
        self.webapp_runner = web.AppRunner(app)
        await self.webapp_runner.setup()
        site = web.TCPSite(self.webapp_runner, platform.node(), self.port)
        await site.start()
        self.logger.info('Serving on %s:%d', platform.node(), self.port)
        print(f'Serving on {platform.node()}:{self.port}')

    async def close(self):
        await self.webapp_runner.cleanup()
        self.logger.info('server closed')
