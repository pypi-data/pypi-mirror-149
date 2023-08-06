import argparse
import inspect
import logging
import pathlib

import simplejson as json
from aiohttp import web
from tinydb import Query, TinyDB  # type: ignore

from arps import __version__ as arps_version
from arps.apps.run_server import RoutesBuilder, run_server

logger = logging.getLogger('policy_poc')

registered_functions = {}

POLICY_DB_PATH = pathlib.Path('arps') / 'apps' / 'policy' / 'policy_db.json'

policy_db = TinyDB(POLICY_DB_PATH)


def register_function(func, description, metadata):
    query = Query()
    result = policy_db.search(query.name == func.__name__)
    if result:
        return

    registered_functions[func.__name__] = func
    policy_db.insert(
        {'name': func.__name__, 'description': description, 'metadata': metadata}
    )


async def dummy_function():
    return web.Response(text='dummy_function')


register_function(
    dummy_function, 'returns a dummy function', inspect.getsource(dummy_function)
)


def load_from_database():
    with open(POLICY_DB_PATH) as db:
        content = json.load(db)

    content = content['_default']
    for _, policies in content.items():
        exec(policies['metadata'])
        registered_functions[policies['name']] = eval(policies['name'])


load_from_database()


async def index(_):
    result = {
        'about': 'Policy Management Tool',
        'version': arps_version,
        'resources': [
            '/list - list all stored policies',
            '/create - opens the resource to create new policies',
        ],
    }

    return web.json_response(result)


async def list_functions(_):
    with open(POLICY_DB_PATH) as db:
        content = json.load(db)
    return web.json_response(content['_default'])


async def post_handler(request):
    data = await request.post()
    data = json.loads(data['policy'])
    name = data['name']
    policy_template = """def {name}():
                             import operator
                             if operator.{operator}(sensors['{sensor}'].read(), {threshold}):
                                 actuators['{actuator}'].set({action})
                                 return web.Response(text='policy executed')
                             return web.Response(text='policy not executed')"""

    policy_template = policy_template.format(
        name=name,
        sensor=data['sensor'],
        operator=data['operator'],
        threshold=data['threshold'],
        actuator=data['actuator'],
        action=data['action'],
    )

    exec(policy_template)
    register_function(eval(name), data['description'], policy_template)
    return web.json_response('post handler called')


def create(_):
    return web.HTTPFound('/create_policy.html')


def setup_route():
    # TODO: review this post with identity crisis since it is in a get
    # route
    get_routes = {
        r'/': index,
        r'/list': list_functions,
        r'/create': create,
        r'/post': post_handler,
    }
    routes_builder = RoutesBuilder()
    routes_builder.add_get(get_routes)

    static_folder = pathlib.Path(pathlib.os.path.dirname(__file__)) / 'static'
    static_routes = {r'/': static_folder}
    return routes_builder.routes, static_routes


def create_agents_directory_config_file(address, port):
    path = pathlib.Path(pathlib.os.path.dirname(pathlib.os.path.abspath(__file__)))
    path = path / 'static' / 'agents_directory_config.json'
    with open(str(path), 'w+') as config_file:
        json.dump({'ad_address': address, 'ad_port': port}, config_file)
        config_file.write('\n')


def build_program_args():
    argparser = argparse.ArgumentParser('Policy Management Tool')
    argparser.add_argument(
        '-a',
        '--agents_directory_address',
        default='127.0.0.1',
        help='address where agents directory is located',
    )
    argparser.add_argument(
        '-ap',
        '--agents_directory_port',
        default=1500,
        help='port where agents directory is listening',
    )
    argparser.add_argument(
        '-p',
        '--port',
        default=8000,
        help='port where Policy Management Tool will listen',
    )
    return argparser


def main():
    argparser = build_program_args()

    parsed_args = argparser.parse_args()

    create_agents_directory_config_file(
        parsed_args.agents_directory_address, parsed_args.agents_directory_port
    )
    routes, static_routes = setup_route()
    run_server(parsed_args.port, routes, static_routes=static_routes)


if __name__ == '__main__':
    main()
