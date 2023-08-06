'''This modules offer methods to be used by all tests and apps that
interact with REST API
'''

import os
import socket
from time import sleep
import urllib
import urllib.request
import urllib.parse
import urllib.error
import platform
from typing import Tuple, Dict, Any, List, Union, Optional, AnyStr
from collections import namedtuple

import simplejson as json

import aiohttp
import psutil  # type: ignore

from arps.apps.run_server import HTTPMethods

HTTPResponse = namedtuple('HTTPResponse', ('code', 'reason'))

JSONType = Union[Dict[str, Any], List[Any], str, int]
WSResponse = Tuple[JSONType, HTTPResponse]


def try_to_connect(address: Optional[str] = None,
                   port: Optional[int] = None,
                   tries: Optional[int] = None):
    '''
    Tries to connect into address:port

    Return True for success or False otherwise

    Args:
    - address: destination address (default platform.node())
    - port: destination port (default 5000)
    - tries: number of times to try to connect (default 5)
    '''

    address = address or platform.node()
    port = port or 5000
    tries = tries or 5

    success = False

    while tries:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sleep(1)
                print('trying to connect into localhost port', port)
                sock.connect((address, port))
                success = True
                break
            except OSError as err:
                print('Error when connecting to', address, ':', port, '->', str(err))
                print('Retrying...')
                tries -= 1

    print('Connected successfully to', port, ':', success)
    return success


def build_url(netloc: str, resource: str, params: Optional[AnyStr] = None):
    request = ('http', netloc, resource, params, None, None)
    return urllib.parse.urlunparse(request)


def build_http_body_and_header(body: Optional[JSONType] = None,
                               headers: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, str]]:
    '''Returns a str of JSON body and make the header describe the data
    as JSON

    '''

    body = json.dumps(body or {})
    headers = headers or {}
    headers['Content-type'] = 'application/json'

    return body, headers


def invoke_rest_ws(method: HTTPMethods,
                   url: str,
                   body: str = None,
                   headers: Dict[str, str] = None,
                   json_resource: bool = True) -> WSResponse:
    bbody = body.encode() if body else b''
    headers = headers or {}
    req = urllib.request.Request(url, data=bbody, headers=headers, method=method.name)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            if json_resource:
                content = json.loads(content.decode())
            return content, HTTPResponse(response.code, response.reason)
    except urllib.error.HTTPError as err:
        content = err.read().decode()
        content = json.loads(content) if content and err.code != 500 else {}
        return content, HTTPResponse(err.code, err.reason)
    except urllib.error.URLError:
        raise RuntimeError(f'Error while accessing resource {url}')


async def async_invoke_rest_ws(method: HTTPMethods,
                               url: str,
                               body: str = None,
                               headers: Dict[str, str] = None,
                               json_resource: bool = True) -> WSResponse:
    '''
    Invoke web service

    Args:
    - method: GET, POST, PUT, or DELETE
    - url: where the resource is located
    - header: HTTP headers if required
    - json_resource: returns the content as JSON object if this flag is True,
    otherwise returns the content as it is

    Raise RuntimeError if service is unaccessible
    '''
    bbody = body.encode() if body else b''
    headers = headers or {}
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        invoke_method = session.get
        if method is HTTPMethods.PUT:
            invoke_method = session.put
        elif method is HTTPMethods.POST:
            invoke_method = session.post
        elif method is HTTPMethods.DELETE:
            invoke_method = session.delete

        try:
            async with invoke_method(url, data=bbody, headers=headers) as response:
                content = await response.text()
                content = json.loads(content) if json_resource else content
                return content, HTTPResponse(response.status, response.reason)
        except aiohttp.ClientResponseError as err:
            return {}, HTTPResponse(err.status, err.message)


def wait_for_process(process, timeout=30):
    '''
    Check for the existence of [process.pid].pid file.
    This file is created by the applications from the apps module

    Args:
    - process: process that has a pid member
    - timeout: time limit to raise TimeoutError
    '''
    assert process.pid in psutil.pids()
    print('Process', process.pid, psutil.Process(process.pid).cmdline())
    pid_file = '{}.pid'.format(process.pid)

    # FIXME Polling: enhance this using some notification module
    count = 0
    while not os.path.exists(pid_file):
        sleep(0.2)
        count += 0.2
        if process.poll() is not None:
            _, error = process.communicate()
            if error:
                error = error.decode().strip()
                raise RuntimeError(error)

        if count > timeout:
            raise TimeoutError(f'Process timeout after {timeout} seconds.')

    print('Process', process.pid, 'has started')


def random_port():
    '''
    Select random available port
    '''
    # https://stackoverflow.com/a/2838309/174605
    # There can be race conditions between the release and the new bind
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]
