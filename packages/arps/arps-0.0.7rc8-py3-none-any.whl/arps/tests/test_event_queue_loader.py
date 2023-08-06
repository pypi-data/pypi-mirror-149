import pathlib
import pytest  # type: ignore
import operator
import itertools

from arps.core.resources_table import ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.event_queue_loader import (FileEventQueueLoader,
                                                    RandomEventQueueLoader)

from arps.test_resources.dummies.dummy_event_factory import (DummyEventFactory,
                                                             DummyEventParamsGenerator)


def dummy_event_factory():
    return DummyEventFactory(ResourcesTable(environment_types={0: 0}),
                             EstimatorsTable())


@pytest.fixture
def event_queue_loader():
    queue_path = pathlib.Path('arps') / 'test_resources' / 'dummies' / 'dummy_jobs.txt'
    return FileEventQueueLoader(queue_path, dummy_event_factory())


def test_number_of_events_in_a_queue(event_queue_loader):
    event_queue = iter(event_queue_loader)
    assert 6 == len(list(event_queue))


def test_as_iterator(event_queue_loader):
    # iterators must be independent
    event_queue0 = iter(event_queue_loader)
    event_queue1 = iter(event_queue_loader)
    event_queue2 = iter(event_queue_loader)
    all_events = list(event_queue0)
    next(event_queue1)
    next(event_queue1)
    result_1 = next(event_queue1)
    result_2 = next(event_queue2)
    assert str(result_1) == str(all_events[2])
    assert str(result_2) == str(all_events[0])


def test_loaded_events_content(event_queue_loader):
    event_queue = iter(event_queue_loader)
    arrival_times = [1, 1, 2, 3, 5, 7]
    for arrival_time, (task_id, event) in zip(arrival_times, enumerate(event_queue, start=1)):
        assert arrival_time == event.arrival_time
        assert event.finished_time is None
        assert task_id == event.identifier


def test_finite_random_events_queue():
    event_queue_loader = RandomEventQueueLoader(dummy_event_factory(),
                                                DummyEventParamsGenerator(),
                                                10)

    event_queue = iter(event_queue_loader)
    events = list(event_queue)
    assert len(events) == 10
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events


def test_infinite_random_events_queue():
    event_queue_loader = RandomEventQueueLoader(dummy_event_factory(),
                                                DummyEventParamsGenerator())

    events = list(itertools.islice(event_queue_loader, 0, 100))
    assert len(events) == 100
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events

    events = list(itertools.islice(event_queue_loader, 0, 10000))
    assert len(events) == 10000
    assert sorted(events, key=operator.attrgetter('arrival_time')) == events


if __name__ == '__main__':
    pytest.main([__file__])
