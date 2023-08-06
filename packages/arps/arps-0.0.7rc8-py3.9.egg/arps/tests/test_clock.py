import asyncio

import pytest # type: ignore

from arps.core.clock import simulator_clock_factory


@pytest.fixture
def clock():
    clock = simulator_clock_factory()
    assert not clock.started
    assert 0 == clock.epoch_time.epoch
    assert clock.epoch_time.valid

    clock.start()
    assert clock.started

    yield clock

    clock.reset()

    assert not clock.epoch_time.valid
    assert not clock.started


@pytest.mark.asyncio
async def test_get_time(clock):
    clock.start()
    assert clock.started

    await clock.update()
    assert 1 == clock.epoch_time.epoch

    assert clock.started
    await clock.update()
    assert 2 == clock.epoch_time.epoch


@pytest.mark.asyncio
async def test_reset(clock):
    for _ in range(10):
        await clock.update()

    assert 10 == clock.epoch_time.epoch
    assert clock.epoch_time.valid

    clock.reset()

    assert not clock.started
    assert 10 == clock.epoch_time.epoch
    assert not clock.epoch_time.valid


@pytest.mark.asyncio
async def test_tick_notification(clock):
    even_counter = 0

    def count_even(_):
        nonlocal even_counter
        even_counter += 1

    three_counter = 0

    def count_three(_):
        nonlocal three_counter
        three_counter += 1

    clock.add_listener(count_even,
                       predicate=lambda time_event: time_event.value % 2 == 0)
    clock.add_listener(count_three,
                       predicate=lambda time_event: time_event.value % 3 == 0)

    while clock.epoch_time.epoch < 10:
        await clock.update()

    await clock.wait_for_notified_tasks()

    assert clock.started

    assert 5 == even_counter
    assert 3 == three_counter


@pytest.mark.asyncio
async def test_run_clock(clock):
    future = asyncio.Future()

    async def wait_for_result(time_event):
        if time_event.value == 5:
            future.set_result('wait done')

    clock.add_listener(wait_for_result)
    clock_task = asyncio.create_task(clock.run())

    assert not future.done()
    await future
    assert future.done()
    assert future.result() == 'wait done'

    clock_task.cancel()

    await clock_task

    assert clock.epoch_time.epoch == 5

if __name__ == '__main__':
    pytest.main([__file__])
