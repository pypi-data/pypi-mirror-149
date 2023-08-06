import platform
from http import HTTPStatus

import pytest # type: ignore

from arps.core.real.rest_api_utils import (build_url,
                                           invoke_rest_ws,
                                           HTTPMethods)
from arps.test_resources.apps_runner import start_pmt_service


def test_main():
    with start_pmt_service() as pmt_port:
        address = f'{platform.node()}:{pmt_port}'
        result, response = invoke_rest_ws(HTTPMethods.GET, build_url(address))
        assert response.code == HTTPStatus.OK
        assert 'about' in result and 'resources' in result


if __name__ == '__main__':
    pytest.main([__file__])
