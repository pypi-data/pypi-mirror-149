import sys
import logging

from arps.test_resources.check_for_apps import check_for_apps

# output from all tests are stored in this file
logging.basicConfig(filename='unit_tests_output.log', level=logging.INFO)
logger = logging.getLogger('run_all_tests')


def pytest_configure(config):
    sys._called_from_test = True


def pytest_unconfigure(config):
    del sys._called_from_test


def pytest_sessionstart(session):
    result, message = check_for_apps()

    if not result:
        sys.exit(message)
