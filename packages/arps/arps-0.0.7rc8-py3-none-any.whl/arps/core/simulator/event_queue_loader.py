import pathlib
import os
from typing import Callable, Any, Optional, Iterator
from collections.abc import Iterable

from arps.core.simulator.event_factory import EventFactory
from arps.core.simulator.sim_event import SimEvent


class EventQueueLoader(Iterable):
    '''Base class
    '''


class FileEventQueueLoader(EventQueueLoader):
    '''This class loads the queue that will contain events.

    This class assumes that the events are ordered by arrival time.

    '''

    def __init__(self, path: pathlib.Path, event_factory: EventFactory) -> None:
        '''Args:
        - path: where the event queue file is loacated
        - event_factory: instance that builds events based on each entry
          in the event queue file
        '''
        self.path = path
        self.event_factory = event_factory

    def __iter__(self) -> Iterator[Optional[SimEvent]]:
        '''
        Load queue from one or more files
        '''
        if not os.path.getsize(self.path):
            return iter([])

        def iterator():
            with open(self.path) as event_queue_fh:
                for line in event_queue_fh:
                    if not line:
                        continue
                    event_params = line.strip('\n').split(' ')
                    yield self.event_factory(*event_params)
        return iterator()


class RandomEventQueueLoader(EventQueueLoader):

    def __init__(self, event_factory: EventFactory,
                 random_params: Callable[[], Any], number_of_events: Optional[int] = None) -> None:
        '''Initialize RandomEventQueueLoader

        Args:
        - events_loader: sequence of EventLoader
        - event_factory: instance that builds events based on each entry
          in the event queue file
        - number_of_events: how many random events should be generated
        '''
        self.number_of_events = number_of_events
        self.event_factory = event_factory
        self.random_params = random_params

    def __iter__(self) -> Iterator[Optional[SimEvent]]:
        '''Return an event from event_factory and its random parameters

        If number_of_events is set, it will generate this number of
        events. Otherwise, it will run indefinitely

        '''

        if self.number_of_events is None:
            def generate_events_indefinitely():
                while True:
                    yield self.event_factory(*self.random_params())
            return generate_events_indefinitely()

        return (self.event_factory(*self.random_params()) for _ in range(self.number_of_events))
