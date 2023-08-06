from io import StringIO
from logging import StreamHandler

import pytest # type: ignore

from arps.core.metrics_logger import (MetricsLogger,
                                      NumberOfMessagesMetric,
                                      PolicyEvaluatedMetric)
from arps.core.remove_logger_files import remove_logger_files


# pylint: disable=no-member
def test_number_of_messages():
    stream = StringIO()
    log_handler = StreamHandler(stream)
    metrics_logger = MetricsLogger(0, log_handler)
    metrics_logger.add(NumberOfMessagesMetric)

    assert metrics_logger.number_of_messages() == 0
    metrics_logger.update_number_of_messages()
    metrics_logger.update_number_of_messages()

    assert metrics_logger.number_of_messages() == 2
    assert stream.getvalue()[:-1].split('\n') == ['NumberOfMessagesMetric -> 1', 'NumberOfMessagesMetric -> 2']

    remove_logger_files(metrics_logger.logger)


def test_policies_executed():
    stream = StringIO()
    log_handler = StreamHandler(stream)

    metrics_logger = MetricsLogger(0, log_handler)
    metrics_logger.add(PolicyEvaluatedMetric)

    assert metrics_logger.policies_evaluated() == {}
    metrics_logger.update_policies_evaluated('Dummy', 0)

    metrics_logger.update_policies_evaluated('Dummy', 1)

    metrics_logger.update_policies_evaluated('AnotherDummy', 4)
    assert metrics_logger.policies_evaluated() == {'Dummy': 2, 'AnotherDummy': 1}

    remove_logger_files(metrics_logger.logger)


if __name__ == '__main__':
    pytest.main([__file__])
