import sys
import asyncio
import pytest  # type: ignore
import threading
from queue import Queue
import urllib.request
import urllib.parse
from http import HTTPStatus
import os
import signal
import platform
from collections import namedtuple
from typing import List, Tuple, Any
import traceback

import simplejson as json
from aiohttp import web

from arps.apps.run_server import run_server, RoutesBuilder, HTTPMethods
from arps.core.real.rest_api_utils import (try_to_connect,
                                           random_port,
                                           build_url,
                                           build_http_body_and_header,
                                           invoke_rest_ws)

ok_response = 'resource at /{uid}: {message}'
error_response = 'resource /{uid} not found'


class Server:
    '''
    Simple server supporting GET, POST, PUT, DELETE methods
    '''
    def __init__(self):
        self.resource = {0: 'default'}
        self._response_template = namedtuple('response', 'message')

    def response_template(self, message):
        return self._response_template(message)._asdict()

    async def get(self, request):
        uid = int(request.match_info['uid'])
        if uid not in self.resource.keys():
            return web.json_response(self.response_template(error_response.format(uid=uid)), status=HTTPStatus.NOT_FOUND)

        return web.json_response(self.response_template(ok_response.format(uid=uid, message=self.resource[uid])))

    async def post(self, request):
        content = await request.content.read()
        content = json.loads(content.decode())
        new_message = content['message']
        new_uid = max(int(i) for i in self.resource.keys()) + 1
        self.resource[new_uid] = new_message
        return web.json_response(self.response_template(ok_response.format(uid=new_uid, message=new_message)), status=HTTPStatus.CREATED)

    async def put(self, request):
        uid = int(request.match_info['uid'])
        if uid not in self.resource.keys():
            return web.json_response(self.response_template(error_response.format(uid=uid)), status=HTTPStatus.NOT_FOUND)

        content = await request.content.read()
        content = json.loads(content.decode())
        new_message = content['message']
        self.resource[uid] = new_message
        return web.json_response(self.response_template(ok_response.format(uid=uid, message=new_message)), status=HTTPStatus.OK)

    async def delete(self, request):
        uid = int(request.match_info['uid'])
        message = self.resource.get(uid, None)
        self.resource.pop(uid, None)

        return web.json_response(self.response_template(ok_response.format(uid=uid, message=message)), status=HTTPStatus.OK)


def run_client(queue: Queue, port: int, requests: List[Tuple[Any]]):
    assert try_to_connect(address=platform.node(), port=port)

    try:
        for request in requests:
            method, expected_response, *_ = request
            expected_message, expected_status = expected_response
            assert method in HTTPMethods
            url = lambda resource: build_url(f'{platform.node()}:{port}', resource)
            if method in [HTTPMethods.GET, HTTPMethods.DELETE]:
                *_, uid = request
                content, response = invoke_rest_ws(method, url(f'/test/{uid}'))
            elif method is HTTPMethods.POST:
                *_, method_params = request
                content, response = invoke_rest_ws(method, url(f'/test'), **method_params)
            elif method is HTTPMethods.PUT:
                *_, uid, method_params = request
                content, response = invoke_rest_ws(method, url(f'/test/{uid}'), **method_params)
            else:
                assert False, f'Method not implemented {method.name}'

            assert response.code == expected_status, response.reason
            assert content['message'] == expected_message

        queue.put((True, 'passed'))
    except (urllib.request.HTTPError, AssertionError) as err:
        queue.put((False, f'failed: {extract_exception_info()}, message: {err}'))
    except Exception as err:
        queue.put((False, f'error: {extract_exception_info()}, message: {err}'))
    finally:
        os.kill(os.getpid(), signal.SIGINT)


def extract_exception_info():
    *_, tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]

    return f'{filename}:{line} in statement {text}'


def setup_server_validate_client_requests(client_requests, server_port, server_routes):
    '''
    Setup server_routes and start REST server listening at server_port.

    Send each one of the requests in client_requests in the order that it was received

    Args:
    - client_requests: list containing requests to be executed by the client
    - server_port: port to listen
    - server_routes: mapping between resource and handler
    '''

    queue = Queue(1)
    thread_requests = threading.Thread(target=run_client,
                                       args=(queue, server_port,
                                             client_requests))
    thread_requests.start()

    try:
        run_server(server_port, server_routes)
    except RuntimeError as err:
        print('Runtime error:', str(err))

    thread_requests.join()

    result, message = queue.get()
    assert result, message


@pytest.fixture
def setup():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    server = Server()
    routes_builder = RoutesBuilder()

    yield server, routes_builder

    loop.close()


def test_get(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})

    port = random_port()

    requests = [(HTTPMethods.GET, (ok_response.format(uid=0, message='default'), HTTPStatus.OK), 0)]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


def test_get_invalid_resource(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})

    port = random_port()

    requests = [(HTTPMethods.GET, (error_response.format(uid=1), HTTPStatus.NOT_FOUND), 1)]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


def test_post(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})
    routes_builder.add_post({'/test': server.post})

    port = random_port()

    body, headers = build_http_body_and_header({'message': 'banana'})

    requests = [(HTTPMethods.GET, (ok_response.format(uid=0, message='default'), HTTPStatus.OK), 0),
                (HTTPMethods.POST, (ok_response.format(uid=1, message='banana'), HTTPStatus.CREATED), {'headers': headers, 'body': body}),
                (HTTPMethods.GET, (ok_response.format(uid=0, message='default'), HTTPStatus.OK), 0),
                (HTTPMethods.GET, (ok_response.format(uid=1, message='banana'), HTTPStatus.OK), 1)]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


def test_put(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})
    routes_builder.add_post({'/test': server.post})
    routes_builder.add_put({'/test/{uid}': server.put})

    port = random_port()

    body, headers = build_http_body_and_header({'message': 'banana'})

    requests = [(HTTPMethods.GET, (ok_response.format(uid=0, message='default'), HTTPStatus.OK), 0),
                (HTTPMethods.PUT, (ok_response.format(uid=0, message='banana'), HTTPStatus.OK), 0, {'headers': headers, 'body': body}),
                (HTTPMethods.GET, (ok_response.format(uid=0, message='banana'), HTTPStatus.OK), 0)]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


def test_put_failed(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})
    routes_builder.add_post({'/test': server.post})
    routes_builder.add_put({'/test/{uid}': server.put})

    port = random_port()

    body, headers = build_http_body_and_header({'message': 'banana'})

    requests = [(HTTPMethods.PUT, (error_response.format(uid=1), HTTPStatus.NOT_FOUND), 1, {'headers': headers, 'body': body})]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


def test_delete(setup):
    server, routes_builder = setup
    routes_builder.add_get({'/test/{uid}': server.get})
    routes_builder.add_post({'/test': server.post})
    routes_builder.add_put({'/test/{uid}': server.put})
    routes_builder.add_delete({'/test/{uid}': server.delete})

    port = random_port()

    body, headers = build_http_body_and_header({'message': 'banana'})

    requests = [(HTTPMethods.POST, (ok_response.format(uid=1, message='banana'), HTTPStatus.CREATED), {'headers': headers, 'body': body}),
                (HTTPMethods.GET, (ok_response.format(uid=1, message='banana'), HTTPStatus.OK), 1),
                (HTTPMethods.DELETE, (ok_response.format(uid=1, message='banana'), HTTPStatus.OK), 1),
                (HTTPMethods.GET, (error_response.format(uid=1), HTTPStatus.NOT_FOUND), 1),
                (HTTPMethods.DELETE, (ok_response.format(uid=1, message=None), HTTPStatus.OK), 1)]

    setup_server_validate_client_requests(requests, port, routes_builder.routes)


if __name__ == '__main__':
    pytest.main([__file__])
