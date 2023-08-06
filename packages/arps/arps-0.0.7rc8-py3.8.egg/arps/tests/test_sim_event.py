import pytest  # type: ignore
from contextlib import suppress

from arps.core.simulator.sim_event import SimEvent


class StatefulSimEvent(SimEvent):
    def __init__(self, identifier, arrival_time, remaining_time):
        self.state = 'created'
        super().__init__(identifier=identifier,
                         arrival_time=arrival_time,
                         remaining_time=remaining_time,
                         event_specific_info='some specific property')

    def main_task(self, epoch):
        self.state = f'main {epoch}'
        return True

    def pos(self, epoch):
        self.state = f'pos {epoch}'


def test_info():
    event = StatefulSimEvent(identifier=1, arrival_time=1, remaining_time=1)
    assert event.info == 'some specific property'


def test_event_consumption_of_duration_one():
    event = StatefulSimEvent(identifier=1, arrival_time=1, remaining_time=1)

    assert event.arrival_time == 1
    assert event.finished_time is None
    assert not event.scheduled

    event.schedule(1, 0)
    assert event.scheduled

    proc = event.process()
    proc.send(None)

    assert event.finished_time is None

    with suppress(StopIteration):
        proc.send(1)

    assert event.finished_time is not None


def test_event_process():
    epoch = 0
    event = StatefulSimEvent(identifier=1, arrival_time=1, remaining_time=5)
    event.schedule(1, epoch)

    proc = event.process()
    proc.send(None)

    states = iter(['created', 'main 1', 'main 2', 'main 3', 'main 4', 'pos 5'])

    assert event.state == next(states)

    while True:
        epoch += 1
        try:
            proc.send(epoch)
        except StopIteration:
            break
        else:
            assert next(states) == event.state


def test_event_process_parallel():
    events = [StatefulSimEvent(identifier=1, arrival_time=1, remaining_time=5),
              StatefulSimEvent(identifier=2, arrival_time=1, remaining_time=5)]

    procs = list()
    for event in events:
        event.schedule(1, 0)
        proc = event.process()
        proc.send(None)
        procs.append(proc)

    states = iter(['created', 'main 1', 'main 2', 'main 3', 'main 4', 'pos 5'])

    epoch = 0
    for current_state in states:
        assert events[0].state == current_state
        assert events[1].state == current_state
        epoch += 1

        for proc in procs:
            try:
                proc.send(epoch)
            except StopIteration:
                continue


def test_not_boolean_main_task():
    class IncorrectSimEvent(SimEvent):
        def main_task(self, epoch):
            return

    event = IncorrectSimEvent(identifier=1, arrival_time=1, remaining_time=1)
    proc = event.process()
    event.schedule(1, 0)

    proc.send(None)
    with pytest.raises(AssertionError) as err:
        proc.send(1)
        assert err == 'main task should return a boolean'


def test_reset():
    event = StatefulSimEvent(identifier=1, arrival_time=1, remaining_time=1)

    assert not event.scheduled
    event.schedule(1, 0)
    assert event.scheduled
    assert event.finished_time is None

    proc = event.process()
    proc.send(None)

    assert event.finished_time is None
    with suppress(StopIteration):
        proc.send(1)

    assert event.finished_time is not None

    event.reset()
    assert not event.scheduled

    assert event.finished_time is None

    event.schedule(1, 0)
    assert event.scheduled

    proc = event.process()
    proc.send(None)
    assert event.finished_time is None
    with suppress(StopIteration):
        proc.send(1)

    assert event.finished_time is not None


if __name__ == '__main__':
    pytest.main([__file__])
