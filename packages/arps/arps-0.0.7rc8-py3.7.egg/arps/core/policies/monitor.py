'''This module contain a base class that enable agents to monitor a
specific resource

The resource state is saved in disk and it is expected to retrieved
using the way the state is persisted

This is related to metrics_logger module in a way that both are made
to collect data

'''
import logging
from functools import reduce
from io import StringIO
from collections import defaultdict
from typing import List, Tuple
from enum import Enum

import pandas as pd #type: ignore

from arps.core.payload_factory import (PayloadType,
                                       create_action_response)
from arps.core.policy import PeriodicPolicy, ActionType
from arps.core.agent_id_manager import AgentID
from arps.core import logger_setup

MonitorType = Enum('MonitorType', 'Sensor Actuator')


class MonitorPolicy(PeriodicPolicy):
    '''
    This class will periodically gather the resource state
    '''

    def __init__(self, touchpoint_category: str, monitor_type: MonitorType):
        '''The touchpoints are saved on a file named
        monitor_[TOUCHPOINT]_timestamp.log

        '''
        self.touchpoint_category = touchpoint_category
        self.monitor_type = monitor_type
        self.monitor_logger = self._build_monitor_logger()
        self.monitor_logger_path = self.monitor_logger.handlers[0].baseFilename
        super().__init__()

    def _build_monitor_logger(self):
        '''
        Build each monitor logger
        '''
        logger = logging.getLogger(self.touchpoint_category)
        logger_setup.set_to_rotate(logger, f'monitor_{self.touchpoint_category}',
                                   header_field=self.touchpoint_category)
        return logger

    def _condition(self, host, event, epoch) -> bool:
        is_periodic = event.type == PayloadType.periodic_action
        is_action = event.type == PayloadType.action
        return (is_periodic and event.content == id(self)) or is_action


    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        if event.type == PayloadType.periodic_action:
            return self.log_touchpoint(host)

        if event.type == PayloadType.action:
            return self.create_action_response(host, event)

        raise RuntimeError(f"It is not supposed to reach this state. Payload type {event['request']['type']}")

    def log_touchpoint(self, host):
        if self.monitor_type is MonitorType.Sensor:
            sensor_state = host.read_sensor(self.touchpoint_category)
            self.monitor_logger.info(sensor_state)

        if self.monitor_type is MonitorType.Actuator:
            actuator_state = host.read_actuator(self.touchpoint_category)
            self.monitor_logger.info(actuator_state)

        return (ActionType.result, True)

    def create_action_response(self, host, request):
        sender_id = request.sender_id
        receiver_id = request.receiver_id
        message_id = request.message_id
        message = create_action_response(receiver_id, sender_id,
                                         self.monitor_logger_path, message_id)
        return (ActionType.event, host.send(message,
                                            AgentID.from_str(sender_id)))


def build_monitor_policy_class(name, touchpoint_category: str,
                               monitor_type: MonitorType):

    def monitor_policy_init(self):
        super(self.__class__, self).__init__(touchpoint_category, monitor_type)

    return type(name, (MonitorPolicy,), {'__init__': monitor_policy_init})


def merge_monitor_logs(logs: List[str]) -> str:
    '''
    Merge multiple logs from monitors into a single log. Each monitor will have its own column in a CSV file

    Args:
    - logs: list of path to the logs
    '''
    if not logs:
        return ''

    logs_as_csv = [pd.read_csv(log, sep=';').drop('level', axis=1) for log in logs]

    #Add a new column to make it easier to merge columns based on time
    add_count_time_into_logs(logs_as_csv)

    result = reduce(lambda left, right: pd.merge(left, right, how='outer', on=['date', 'time', 'count_time']), logs_as_csv)
    result.drop('count_time', axis=1, inplace=True)
    result.sort_values(axis=0, by=['date', 'time'], inplace=True)

    csv_buffer = StringIO()
    result.to_csv(csv_buffer, index=False)

    return csv_buffer.getvalue()


def add_count_time_into_logs(logs_as_csv):
    for log in logs_as_csv:
        log['count_time'] = fastcount(log.time.values)


def fastcount(x):
    '''Count occurences in the log. This was done to make it able to
    merge files with repeated values

    '''
    def cg(x):
        cnt = defaultdict(lambda: 0)

        for j in x.tolist():
            cnt[j] += 1
            yield cnt[j]

    return [i for i in cg(x)]
