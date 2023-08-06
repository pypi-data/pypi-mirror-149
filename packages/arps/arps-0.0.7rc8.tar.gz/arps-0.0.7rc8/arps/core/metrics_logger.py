'''
This module refers to metrics that can be collected by agents about their
internal state by accessing their attributes.

To collect metrics regarding resources see arps/core/policies/monitor.py
since it will be performed by the Monitor step of MAPE loop control. This
loop control is what drives the agent.
'''

from collections import defaultdict
import logging
from datetime import datetime


class MetricsLoggers:

    def __init__(self):
        self._loggers = dict()

    def register(self, identifier):
        logger = MetricsLogger(identifier)
        self._loggers[identifier] = logger
        return logger

    def loggers(self):
        return self._loggers


class MetricsLogger:

    def __init__(self, agent_identifier, log_handler=None):
        '''
        Log information related to agents activities

        So far:
        - number of messages: messages received by agent
        - policies whose conditon has met

        Args:
        - agent_identifier: unique agent identifier
        '''
        self.agent_id = agent_identifier

        self.logger = None
        self._setup_log(log_handler)
        self.add(NumberOfMessagesMetric)

    def add(self, metric_cls):
        metric_instance = metric_cls()
        setattr(MetricsLogger, metric_cls.name, metric_instance)

        def update_and_log(self, *args, **kwargs):
            metric_instance.update(*args, **kwargs)
            self.logger.info('%s -> %s', metric_cls.__name__, metric_instance())
        setattr(MetricsLogger, 'update_' + metric_cls.name, update_and_log)

    def _setup_log(self, log_handler):
        self.logger = logging.getLogger('Metrics_{}'.format(self.agent_id))
        self.logger.setLevel(logging.INFO)

        current_time = datetime.now().strftime('%Y%m%d-%H%M%S.%f')
        file_handler = logging.FileHandler(f'metrics_agent_{self.agent_id}_{current_time}.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if log_handler:
            self.logger.addHandler(log_handler)

    def __hash__(self):
        return hash(self.agent_id)

    def __eq__(self, other):
        return self.agent_id == other.agent_id


class Metric:
    '''Base metric class

    '''


class NumberOfMessagesMetric(Metric):
    name = 'number_of_messages'

    def __init__(self):
        self._number_of_messages = 0

    def __call__(self):
        return self._number_of_messages

    def update(self):
        self._number_of_messages += 1


class PolicyEvaluatedMetric(Metric):
    name = 'policies_evaluated'

    def __init__(self):
        self.policy_evaluated = defaultdict(int)

    def __call__(self):
        return self.policy_evaluated

    def update(self, policy_name, time):
        '''
        Stores a list of epoch time that indicates when a policy was evaluated as True

        Args:
        - policy_name : name to identify policy
        - time: when the policy was evaluated
        '''
        self.policy_evaluated[policy_name] += 1
