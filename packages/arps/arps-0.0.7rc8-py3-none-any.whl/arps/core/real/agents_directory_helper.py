import logging
from functools import partial
from http import HTTPStatus
from typing import Dict, Optional

from arps.core.real.rest_api_utils import (invoke_rest_ws,
                                           build_url,
                                           build_http_body_and_header,
                                           HTTPMethods,
                                           JSONType)


class AgentsDirectoryHelperError(Exception):
    '''Exception to describe a problem during the execution of a request

    '''


class AgentsDirectoryHelper:

    def __init__(self, *, address: str, port: int) -> None:
        '''
        Initialize connection to the agents directory

        Args:
        - address: url to access the agents directory
        - port: port being listened by the agents directory
        '''
        self.port = port
        address = '{}:{}'.format(address, self.port)
        self.endpoint = partial(build_url, address)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get(self, *, agent_id: str) -> JSONType:
        '''Get info about agent in agents directory
        '''
        return self.request(HTTPMethods.GET, f'agents/{agent_id}')

    def add(self, *, agent_id: str, address: str, port: int) -> JSONType:
        '''Add info about agent in agents directory
        '''

        body = {'id': agent_id, 'address': address, 'port': str(port)}
        return self.request(HTTPMethods.PUT, 'agents', body)

    def remove(self, *, agent_id: str) -> JSONType:
        '''Remove agent from agents directory
        '''
        return self.request(HTTPMethods.DELETE, f'agents/{agent_id}')

    def list(self) -> JSONType:
        '''List registered agents
        '''
        return self.request(HTTPMethods.GET, 'agents')

    def about(self) -> JSONType:
        '''Get info about agents directory
        '''
        return self.request(HTTPMethods.GET, 'about')

    def available_commands(self) -> JSONType:
        '''Get available commands in agents directory
        '''
        return self.request(HTTPMethods.GET, '/')

    def request(self, method: HTTPMethods, resource: str,
                body: Optional[Dict[str, str]] = None) -> JSONType:
        new_body, header = build_http_body_and_header(body)
        try:
            result, response = invoke_rest_ws(method, self.endpoint(resource), new_body, header)
        except RuntimeError as err:
            raise AgentsDirectoryHelperError(err)

        if response.code != HTTPStatus.OK:
            raise AgentsDirectoryHelperError(response.reason)

        return result
