import sys
from http import HTTPStatus
import logging
import logging.handlers
import argparse

from aiohttp import web
import simplejson as json

from arps import __version__ as arps_version
from arps.core import logger_setup
from arps.apps.run_server import run_server, RoutesBuilder

# pylint: disable-msg=C0103
logger = logging.getLogger('AgentsDirectory')

agents = {}


async def index(_):
    logger.info('index requested')
    create_agent_payload = "Payload: {'id': 'id_value', 'address': 'address', 'port': 'port'}"
    return web.json_response({'available commands': {'/agents/{id}': 'Retrieves agent (GET) or Removes Agent (DELETE)',
                                                     '/agents': f'List registered agents (GET) or Creates agent (POST). {create_agent_payload}',
                                                     '/about': 'About this service'}})


async def about(_):
    logger.info('about requested')
    return web.json_response(f'agent service directory version {arps_version}')


async def add(request):
    content = await request.content.read()
    content = json.loads(content.decode())

    identifier = str(content.get('id'))
    address = str(content.get('address'))
    port = str(content.get('port'))

    logger.info('add requested')

    if identifier is None or address is None or port is None:
        message = 'Missing id, address, or port parameter'
        logger.info(message)
        return web.json_response(status=HTTPStatus.BAD_REQUEST, reason=message)

    if identifier in agents:
        agent_info = agents[identifier]
        if agent_info['address'] != address or agent_info['port'] != port:
            message = f'Agent {identifier} is already added but with different parameters'
            logger.warning(message)
            return web.json_response(status=HTTPStatus.CONFLICT, reason=message)

    agents[identifier] = {'address': address, 'port': port}
    message = f'Agent {identifier} added'
    logger.info(message)
    logger.info(agents[identifier])
    return web.json_response(message)


async def get(request):
    agent_id = request.match_info.get('agent_id')

    logger.info('get requested')

    if agent_id not in agents:
        message = f'Agent {agent_id} not found'
        logger.info(message)
        return web.json_response(status=HTTPStatus.NOT_FOUND, reason=message)

    logger.info(agents[agent_id])
    return web.json_response(data=agents[agent_id])


async def remove(request):
    agent_id = request.match_info.get('agent_id')

    logger.info('remove requested')

    if agent_id not in agents:
        message = f'Agent {agent_id} not found'
        logger.info(message)
        return web.json_response(status=HTTPStatus.NOT_FOUND, reason=message)

    del agents[agent_id]
    message = f'Agent {agent_id} removed'
    logger.info(message)
    return web.json_response(data=message)


async def list_agents(_):
    logger.info('list agents: %s', agents)
    return web.json_response(data=agents, headers={'Access-Control-Allow-Origin': '*'})


def parse_arguments():
    parser = argparse.ArgumentParser('Runs agent directory service.')
    parser.add_argument('--port', type=int, default=1500, help='port to listen')
    parser.add_argument('--quiet', default=False,
                        action='store_const', const=True, help='No log generated')
    parser.add_argument('--version', action='version', version=f'ARPS {arps_version}')

    return parser.parse_args(sys.argv[1:])


def main():
    parsed_args = parse_arguments()

    if not parsed_args.quiet:
        logger_setup.set_to_rotate(logger, file_name_prefix='agents_directory')

    get_routes = {r'/': index,
                  r'/agents/{agent_id}': get,
                  r'/agents': list_agents,
                  r'/about': about}

    put_routes = {r'/agents': add}

    delete_routes = {r'/agents/{agent_id}': remove}

    routes_builder = RoutesBuilder()
    routes_builder.add_get(get_routes)
    routes_builder.add_put(put_routes)
    routes_builder.add_delete(delete_routes)

    try:
        run_server(parsed_args.port, routes_builder.routes)
        logger.info('rest service has stopped')
        sys.exit(0)
    except RuntimeError as err:
        logger.info(str(err))
        sys.exit(str(err))


if __name__ == '__main__':
    main()
