import asyncio
from enum import Enum
from functools import partial

import pytest  # type: ignore

from arps.core.observable_mixin import ObservableMixin, StochasticObservableMixin

ObservableEvents = Enum('ObservableEvents', 'event_one event_two event_three')


@pytest.mark.asyncio
async def test_observable_mixin_workflow():

    observer = ObservableMixin()

    events = list()
    other_events = list()
    run_event = 0

    def run():
        nonlocal run_event
        run_event += 1

    observer.add_listener(events.append)
    observer.add_listener(other_events.append)
    observer.add_listener(run)

    observer.notify('test')
    await observer.wait_for_notified_tasks()

    assert events.count('test') == 1
    assert other_events.count('test') == 1
    assert run_event == 1

    observer.notify('test')
    observer.notify('test')
    observer.notify('test')

    await observer.wait_for_notified_tasks()

    assert events.count('test') == 4
    assert other_events.count('test') == 4
    assert run_event == 4


@pytest.mark.asyncio
async def test_conditional_listeners():

    observer = ObservableMixin()

    str_events = list()
    int_events = list()

    observer.add_listener(str_events.append, predicate=lambda event: isinstance(event, str))
    observer.add_listener(int_events.append, predicate=lambda event: isinstance(event, int))

    expected_ints = list(range(10))
    expected_strs = [str(i) for i in expected_ints]

    for i in range(10):
        observer.notify(i)
        observer.notify(str(i))

    await observer.wait_for_notified_tasks()

    assert int_events == expected_ints
    assert str_events == expected_strs


@pytest.mark.asyncio
async def test_observables_mixin_workflow():
    observer_one = ObservableMixin()
    observer_two = ObservableMixin()

    one_id = id(observer_one)
    two_id = id(observer_two)

    async def notify_both():
        observer_one.notify(one_id)
        observer_two.notify(two_id)
        await observer_one.wait_for_notified_tasks()
        await observer_two.wait_for_notified_tasks()

    await observer_one.wait_for_notified_tasks()
    await observer_two.wait_for_notified_tasks()

    events = list()
    other_events = list()
    run_event = 0

    def run():
        nonlocal run_event
        run_event += 1

    observer_one.add_listener(events.append)
    observer_two.add_listener(events.append)
    observer_one.add_listener(other_events.append)
    observer_one.add_listener(run)
    observer_two.add_listener(run)

    await notify_both()

    assert events.count(one_id) == 1
    assert events.count(two_id) == 1
    assert other_events.count(one_id) == 1
    assert two_id not in other_events
    assert run_event == 2

    await notify_both()
    await notify_both()
    await notify_both()

    assert events.count(one_id) == 4
    assert events.count(two_id) == 4
    assert other_events.count(one_id) == 4
    assert two_id not in other_events
    assert run_event == 8


@pytest.mark.asyncio
async def test_observables_mixin_remove_listener():
    observer_one = ObservableMixin()
    observer_two = ObservableMixin()

    one_id = id(observer_one)
    two_id = id(observer_two)

    async def notify_both():
        observer_one.notify(one_id)
        observer_two.notify(two_id)
        await observer_one.wait_for_notified_tasks()
        await observer_two.wait_for_notified_tasks()

    events = list()
    run_event = 0

    def run():
        nonlocal run_event
        run_event += 1

    observer_one.add_listener(events.append)
    observer_two.add_listener(events.append)
    observer_one.add_listener(run)
    observer_two.add_listener(run)

    await notify_both()

    assert events.count(one_id) == 1
    assert events.count(two_id) == 1
    assert run_event == 2

    await notify_both()

    assert events.count(one_id) == 2
    assert events.count(two_id) == 2
    assert run_event == 4

    observer_one.remove_listener(events.append)

    await notify_both()

    assert events.count(one_id) == 2
    assert events.count(two_id) == 3
    assert run_event == 6

    observer_two.remove_listener(run)

    await notify_both()

    assert events.count(one_id) == 2
    assert events.count(two_id) == 4
    assert run_event == 7


@pytest.mark.asyncio
async def test_listeners_order_execution_same_priority():
    observer = ObservableMixin()

    events_one = list()
    events_two = list()
    events_three = list()
    order = 0

    def append(event_list, event):
        nonlocal order
        order += 1
        event_list.append((event, order))

    observer.add_listener(partial(append, events_one))
    observer.add_listener(partial(append, events_two))
    observer.add_listener(partial(append, events_three))

    for i in range(10):
        observer.notify(i)
        await observer.wait_for_notified_tasks()

    assert events_one and events_one == [(i, j) for i, j in zip(range(10), range(1, 30, 3))]
    assert events_two and events_two == [(i, j) for i, j in zip(range(10), range(2, 30, 3))]
    assert events_three and events_three == [(i, j) for i, j in zip(range(10), range(3, 31, 3))]


@pytest.mark.asyncio
async def test_listeners_order_execution_different_priority():
    observer = ObservableMixin()

    events_one = list()
    events_two = list()
    events_three = list()
    order = 0

    def append(event_list, event):
        nonlocal order
        order += 1
        event_list.append((event, order))

    observer.add_listener_low_priority(partial(append, events_one))
    observer.add_listener(partial(append, events_two))
    observer.add_listener(partial(append, events_three))

    for i in range(10):
        observer.notify(i)
        await observer.wait_for_notified_tasks()

    # events_one executes after events_two and events_three
    assert events_one and events_one == [(i, j) for i, j in zip(range(10), range(3, 31, 3))]
    assert events_two and events_two == [(i, j) for i, j in zip(range(10), range(1, 30, 3))]
    assert events_three and events_three == [(i, j) for i, j in zip(range(10), range(2, 30, 3))]


@pytest.mark.asyncio
async def test_listeners_random_order_execution_same_priority():
    observer = StochasticObservableMixin()

    events_one = list()
    events_two = list()
    events_three = list()
    order = 0

    def append(event_list, event):
        nonlocal order
        order += 1
        event_list.append((event, order))

    observer.add_listener(partial(append, events_one))
    observer.add_listener(partial(append, events_two))
    observer.add_listener(partial(append, events_three))

    for i in range(10):
        observer.notify(i)
        await observer.wait_for_notified_tasks()

    assert events_one and events_one != [(i, j) for i, j in zip(range(10), range(1, 30, 3))]
    assert events_two and events_two != [(i, j) for i, j in zip(range(10), range(2, 30, 3))]
    assert events_three and events_three != [(i, j) for i, j in zip(range(10), range(3, 31, 3))]


@pytest.mark.asyncio
async def test_async_callback_that_exceeds_timeout():
    observer = StochasticObservableMixin(timeout=1)

    slow = asyncio.Event()
    fast = asyncio.Event()

    async def slow_callback(_):
        await asyncio.sleep(2)
        slow.set()

    async def fast_callback(_):
        await asyncio.sleep(0.5)
        fast.set()

    observer.add_listener(slow_callback)
    observer.add_listener(fast_callback)

    observer.notify(None)
    await observer.wait_for_notified_tasks()

    assert not slow.is_set()
    assert fast.is_set()


if __name__ == '__main__':
    pytest.main([__file__])
