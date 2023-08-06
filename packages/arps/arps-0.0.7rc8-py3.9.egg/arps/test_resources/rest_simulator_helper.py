import os
import pathlib
import contextlib
import tempfile
import operator
import csv
import itertools
from typing import Tuple, List, Any, Callable
import io
from zipfile import ZipFile
from contextlib import ExitStack

import simplejson as json

from arps.core.real.rest_api_utils import (invoke_rest_ws,
                                           HTTPMethods)

from arps.test_resources.apps_runner import start_agent_manager

LOG_SIMULATOR_RESULTS_FOLDER = pathlib.Path('./log_simulator_tests')


@contextlib.contextmanager
def setup_access_resource(sim_configuration_path, *, quiet=True, debug=False):

    with temp_configuration(str(LOG_SIMULATOR_RESULTS_FOLDER),
                            sim_configuration_path) as sim_environment_file:
        user_defined_parameters = ['--config_file', sim_environment_file]
        with start_agent_manager(user_defined_parameters, quiet, debug) as endpoint:
            yield endpoint


@contextlib.contextmanager
def temp_configuration(log_simulator_results_folder, simulator_conf_path):
    with open(simulator_conf_path, 'r') as conf:
        dummy_simulator_environment = json.loads(conf.read())
        dummy_simulator_environment['simulator']['results_path'] = [log_simulator_results_folder]

        with tempfile.NamedTemporaryFile(suffix='.conf', delete=False, mode='w') as temp_conf:
            json.dump(dummy_simulator_environment, temp_conf.file)
    yield temp_conf.name

    os.remove(temp_conf.name)


def assert_equal_events(expected_results, results, value_comparator=None):
    if len(expected_results) != len(results):
        return False, 'Size differ, got {} as result, expected {}'.format(len(results),
                                                                          len(expected_results))

    value_comparator = value_comparator or operator.eq
    verify = lambda expected, result: value_comparator(expected, result)

    try:
        verified = all(verify(e, r) for e, r in zip(expected_results, results))
    except RuntimeError as err:
        return False, str(err)

    if not verified:
        for e, r in zip(expected_results, results):
            if not verify(e, r):
                return False, 'expected {}, got {}'.format(e, r)

    error_message = 'Unexpected result, check simulation results against expected results'
    return verified, error_message


def retrieve_last_result(sim_access_resource):
    content, response = invoke_rest_ws(HTTPMethods.GET,
                                       sim_access_resource('sim/result'),
                                       json_resource=False)
    assert response.code == 200, f'Got {response.code}, expected 200. Reason: {response.reason}'

    with io.BytesIO(content) as zipfile:
        with ZipFile(zipfile, 'r') as sim_bundle:
            namelist = sim_bundle.namelist()
            metadata = next(name for name in namelist if name.endswith('json'))
            with sim_bundle.open(metadata, 'r') as metadata_file:
                metadata_content = metadata_file.read().decode()

            results_file = next(name for name in namelist if 'sim_results.log' in name)
            events_file = next(name for name in namelist if 'events.log' in name)
            with ExitStack() as exit_stack:
                sim_result_file = exit_stack.enter_context(sim_bundle.open(results_file, 'r'))
                sim_results = _read_csv(sim_result_file)
                sim_results_header = sim_results[0]
                assert len(sim_results_header) == 6, "Simulation results don't match content"

                events_file = exit_stack.enter_context(sim_bundle.open(events_file, 'r'))
                events = _read_csv(events_file)
                events_header = events[0]
                assert len(events_header) == 6, "Simulation events don't match content"

                return metadata_content, sim_results[1:], events[1:]


def _read_csv(csv_file):
    with io.TextIOWrapper(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=';')
        last_sim_result = [tuple(row) for row in csv_reader]

        return last_sim_result


def verify_simulation_results(expected_result: List[Any],
                              last_result: List[Any],
                              value_comparator: Callable[[Any], bool] = None) -> Tuple[bool, str]:

    n_resources = len(list(itertools.takewhile(lambda elem: elem[2] == '0', expected_result))) #get entries which epoch is zero
    last_result[:n_resources] = sorted(last_result[:n_resources]) #because there is no guarantee that will be in the same order
    verified, error_message = assert_equal_events(expected_result, last_result, value_comparator)
    assert verified, error_message
