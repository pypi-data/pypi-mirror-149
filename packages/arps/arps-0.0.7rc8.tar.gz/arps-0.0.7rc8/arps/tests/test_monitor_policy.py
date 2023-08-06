import pytest # type: ignore

from arps.core.policies_executor import ActionType
from arps.core.payload_factory import create_periodic_action
from arps.core.policies.monitor import (build_monitor_policy_class,
                                        MonitorType)
from arps.core.remove_logger_files import remove_logger_files

DummyMonitorPolicy = build_monitor_policy_class('DummyMonitorPolicy',
                                                touchpoint_category='DummySensor',
                                                monitor_type=MonitorType.Sensor)


class DummyAgent:
    async def send(self, content, receiver_id):
        self.content = content
        self.receiver_id = receiver_id


@pytest.fixture
def setup():
    monitor_policy = DummyMonitorPolicy()
    monitor_policy.period = 1
    agent = DummyAgent()
    agent.identifier = '0.1'

    yield agent, monitor_policy

    remove_logger_files(monitor_policy.monitor_logger)


def test_monitor_policy_periodic_action(setup):
    agent, monitor_policy = setup
    result = iter(['dummy1', 'dummy2'])

    agent.read_sensor = lambda _: next(result)
    event = create_periodic_action(id(monitor_policy))
    event_result = monitor_policy.event(host=agent, event=event, epoch=0)
    assert event_result[0] == ActionType.result
    assert event_result[1]

    event_result = monitor_policy.event(host=agent, event=event, epoch=0)
    assert event_result[0] == ActionType.result
    assert event_result[1]

    monitor_path = monitor_policy.monitor_logger.handlers[0].baseFilename
    with open(monitor_path, 'r') as monitored_resource:
        content = monitored_resource.read().splitlines()
        assert len(content) == 3
        assert content[0] == 'date;time;level;DummySensor'
        assert content[1].split(';')[-1] == 'dummy1'
        assert content[2].split(';')[-1] == 'dummy2'


if __name__ == '__main__':
    pytest.main([__file__])
