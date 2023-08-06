import asyncio
import inspect
import logging
import random
from functools import partial, update_wrapper, wraps
from typing import Any, Callable, Optional

Predicate = Callable[[Any], bool]
Callback = Callable[..., None]


class ObservableMixin:
    """This mixin class offers a way to subscribe to events and notify
    listeners

    There are two queue available for notification. One has higher
    priority than the other.

    It offers conditional notifications.

    The order of the notification is the same order that the listeners
    were added.

    """

    def __init__(self, timeout: Optional[int] = None):
        self._high_listeners = list()
        self._low_listeners = list()
        self.notified_tasks = list()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout: int = timeout or 5  # in seconds

    def add_listener(self, listen: Callback, *, predicate: Optional[Predicate] = None) -> None:
        """High priority queue is default"""

        self._add_listener(listen, queue=self._high_listeners, predicate=predicate)

    def add_listener_low_priority(self, listen: Callback, *, predicate: Optional[Predicate] = None) -> None:
        """Low priority queue needs to be called explicitly"""
        self._add_listener(listen, queue=self._low_listeners, predicate=predicate)

    def _add_listener(self, listen: Callback, *, queue, predicate: Optional[Predicate] = None):
        """Add a new listener to track when the resource is modified

        It supports async and non async listeners

        Args:
        - listen: function that will receive an event when the
          resource is modified
        - predicate:
        """
        predicate = predicate or (lambda _: True)
        listener = partial(self.conditional_listener, listen, predicate)
        update_wrapper(listener, listen)
        queue.append(listener)

    def remove_listener(self, listener: Callback) -> None:
        result_low = [_listener for _listener in self._low_listeners if listener == _listener.args[0]]
        result_high = [_listener for _listener in self._high_listeners if listener == _listener.args[0]]
        if result_low:
            result, queue = result_low, self._low_listeners
        elif result_high:
            result, queue = result_high, self._high_listeners
        else:
            return

        if len(result) != 1:
            print('\n'.join(str(element) for element in result))
        assert len(result) == 1, 'Expected 1, got {}: {}'.format(len(result), result)

        queue.remove(result[0])

    def notify(self, event: Any) -> None:
        self.notified_tasks = [task for task in self.notified_tasks if not task.done()]
        for listener in self._high_listeners:
            self.notified_tasks.append(asyncio.create_task(listener(event)))
        for listener in self._low_listeners:
            self.notified_tasks.append(asyncio.create_task(listener(event)))

    async def wait_for_notified_tasks(self):
        try:
            await asyncio.shield(asyncio.wait_for(asyncio.gather(*self.notified_tasks), timeout=self.timeout))
        except asyncio.TimeoutError:
            self.logger.warning('Timeout while waiting notified tasks')
        self.notified_tasks.clear()

    def clear(self):
        self._high_listeners.clear()
        self._low_listeners.clear()

    async def conditional_listener(self, action: Callback, action_condition: Predicate, event: Any) -> None:
        """Execute an action, passing an event as parameter, if condition is
        met

        Args:

        - action: action to be executed (can be sync or async). It
          shouldn't exceed 5 seconds.
        - action_condition: predicate based on the event
        - event: event passed to action

        """

        if not action_condition(event):
            return

        async_action = wrap_into_async(action)

        if len(inspect.signature(action).parameters):
            await async_action(event)
        else:
            await async_action()


def wrap_into_async(sync_or_async: Callback) -> Callable:
    """Wrap the function just to run as async"""
    if asyncio.iscoroutinefunction(sync_or_async):
        return sync_or_async

    @wraps(sync_or_async)
    async def inner(*args, **kwargs):
        return sync_or_async(*args, **kwargs)

    return inner


class StochasticObservableMixin(ObservableMixin):
    """This class offers a way to modify the notification behaviour of
    ObservableMixin.

        The current version offers only the notification order using the
        random.random function
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def notify(self, event):
        random.shuffle(self._high_listeners)
        random.shuffle(self._low_listeners)
        super().notify(event)
