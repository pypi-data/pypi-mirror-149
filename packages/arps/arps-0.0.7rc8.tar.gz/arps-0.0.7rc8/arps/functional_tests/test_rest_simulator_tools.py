import os
import tempfile
from time import sleep
import pathlib
import subprocess
from http import HTTPStatus

import pytest # type: ignore
import simplejson as json

from arps.core.real.rest_api_utils import invoke_rest_ws, HTTPMethods

from arps.test_resources.rest_simulator_helper import setup_access_resource

# pylint:disable=redefined-outer-name


SIM_CONFIG_FILE = pathlib.Path('arps') / 'test_resources' / 'conf' / 'dummy_simulator_environment.conf'


@pytest.fixture
def sim_access_resource():
    with setup_access_resource(SIM_CONFIG_FILE) as partial_uri:
        yield partial_uri


def test_last_sim_result_as_image(sim_access_resource):
    status_endpoint = sim_access_resource('sim/status')
    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    result, response = invoke_rest_ws(HTTPMethods.GET, sim_access_resource('sim/run'))
    assert response.code == HTTPStatus.OK
    assert result == 'running'

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    while result == 'running':
        result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
        assert response.code == HTTPStatus.OK
        sleep(0.15)

    result, response = invoke_rest_ws(HTTPMethods.GET, status_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        sim_result_file = temp_file.name
        sim_last_result_endpoint = sim_access_resource('sim/result')
        result, response = invoke_rest_ws(HTTPMethods.GET,
                                          sim_last_result_endpoint,
                                          json_resource=False)
        assert response.code == HTTPStatus.OK
        temp_file.write(result)

    index_file_path = render_images_from_result(sim_result_file)

    assert_png_images_from_result(index_file_path)

    stop_endpoint = sim_access_resource('sim/stop')
    result, response = invoke_rest_ws(HTTPMethods.GET, stop_endpoint)
    assert response.code == HTTPStatus.OK
    assert result == 'stopped'


def render_images_from_result(result_file_name):
    index_file_path = pathlib.Path(result_file_name).with_suffix('.idx')
    exec_params = ['sim_result_to_image',
                   '--result_file', result_file_name,
                   '--index_file', str(index_file_path)]
    print(' '.join(exec_params))
    returncode = subprocess.call(exec_params)

    assert returncode == 0

    return index_file_path


def assert_png_images_from_result(index_file_path):
    with open(index_file_path) as index_file:
        sim_resources = json.load(index_file)

        assert len(sim_resources['results']) == 8

        for sim_result in sim_resources['results']:
            try:
                with open(sim_result, 'rb') as sim_result_file:
                    assert (os.path.getsize(sim_result_file.name)) > 0

                    #Just to be sure that is a PNG, this will probably
                    #change in the future since I'm still deciding the
                    #right way to retrieve the result of the simulation as
                    #an artifact
                    assert sim_result_file.read(4) == b'\x89PNG'
            finally:
                os.remove(sim_result)
    os.remove(index_file_path)


if __name__ == '__main__':
    pytest.run([__file__])
