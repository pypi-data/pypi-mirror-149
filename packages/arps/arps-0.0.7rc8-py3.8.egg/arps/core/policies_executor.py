import sys
import asyncio
from functools import partial, update_wrapper
import logging
from typing import List, Callable, Any, Tuple, MutableSequence, Dict
from collections import deque

from arps.core.clock import EpochTime, TimeEvent
from arps.core.policy import (ActionType, ReflexPolicy, PeriodicPolicy)
from arps.core.payload_factory import (Payload, create_periodic_action)

CallbackType = Callable[[Any], None]


class PoliciesExecutor:
    def __init__(self, policies: List[ReflexPolicy],
                 epoch_time: EpochTime,
                 clock_callback: Tuple[CallbackType, CallbackType]):
        '''
        Initializes process that deal with policies

        Keyword Args:
        - policies: list of policies that will be used to evaluate received events
        - epoch_time: epoch time to provide info when an event was processed
        '''
        self._policies = policies or list()
        self._epoch_time = epoch_time
        self._events_received: List[Payload] = list()
        self.policy_action_results: MutableSequence[ActionType] = deque(maxlen=50)
        self.received_periodic_events: List[CallbackType] = list()
        self.clock_add_listener, self.clock_remove_listener = clock_callback
        self.logger = logging.getLogger(self.__class__.__name__)
        self.host = None

        self.policies_and_actions: Dict[ReflexPolicy, CallbackType] = dict()
        self._create_periodic_event(self._policies)

    def receive(self, event: Payload):
        '''
        Receive event to be added into the event loop

        Keyword parameters:
        - event : event received in PayloadFactory message format

        '''
        assert self.host
        self.logger.info('event received %s by agent %s', event,
                         self.host.identifier)

        self._events_received.append(event)

    def add_policy(self, policy: ReflexPolicy):
        '''
        Append policy into current policies

        Args:
        - policy: policy instance
        '''
        self._policies.append(policy)
        if isinstance(policy, PeriodicPolicy):
            self._assign_periodic_event_to_policy(policy)

    def remove_policy(self, policy_identifier: str):
        '''
        Removes policy from current policies

        Keyword parameters:
        - policy_identifier: policy's name
        '''

        instances = {
            policy.__class__.__name__: policy
            for policy in self._policies
        }
        policy = instances[policy_identifier]
        self._policies.remove(policy)
        if isinstance(policy, PeriodicPolicy):
            self.clock_remove_listener(self.policies_and_actions[policy])

    @property
    def policies_name(self):
        return [policy.__class__.__name__ for policy in self._policies]

    async def run(self):
        '''event to be called by event loop

        Depending on the type of event:
        - an action can be executed
        - a result can be stored to be retrieve later accessing
          policy_action_results
        '''
        for periodic_event in self.received_periodic_events:
            self.receive(periodic_event)
        self.received_periodic_events.clear()

        policies_result = self._policies_result()
        await self._process_results(policies_result)

    def _policies_result(self):
        '''
        Collect events received and run against current policies

        Returns policies result
        '''
        policies_result = list()

        self.logger.debug('checking for events received: %s', len(self._events_received))
        while self._events_received:
            event_received = self._events_received.pop()
            self.logger.debug('Running event %s on: %s', event_received, self._policies)
            policies_result.extend([
                policy.event(event=event_received,
                             host=self.host,
                             epoch=self._epoch_time.epoch)
                for policy in self._policies
            ])

        return [result for result in policies_result if result]

    async def _process_results(self, policies_result: List[Any]):
        '''
        Process results according to their types

        Event will be execute while an event will be stored
        '''

        while policies_result:
            (action_type, content) = policies_result.pop()
            self.logger.debug('action type to process: %s', action_type.name)

            if action_type == ActionType.event:
                try:
                    self.logger.debug('Content %s', content)
                    if asyncio.iscoroutinefunction(content):
                        await content()
                    elif asyncio.iscoroutine(content):
                        await content
                    else:
                        content()
                    self.logger.debug('action type event executed')
                except GeneratorExit:
                    # ignoring error; should this be done?
                    # I've seen only in tests where this doesn't matter
                    self.logger.error(
                        'Generator Exit: generator/coroutine was closed while awaiting'
                    )
                except Exception as e:
                    self.logger.error('Exception: %s', e)
                    raise e
                except:
                    message = f'Unexpected error: {sys.exc_info()[0]}'
                    raise RuntimeError(message)
                    self.logger.error(message)

            if action_type == ActionType.result:
                self.policy_action_results.append(content)

    def __repr__(self):
        return repr([policy for policy in self._policies])

    def _create_periodic_event(self, policies: List[ReflexPolicy]):
        '''Create periodic action for each periodic policy.

        Add each one of these actions into the clock_callback so
        it can be called when an event occurs

        '''

        periodic_policies = [
            policy for policy in policies if isinstance(policy, PeriodicPolicy)
        ]

        for policy in periodic_policies:
            self._assign_periodic_event_to_policy(policy)

    def _assign_periodic_event_to_policy(self, policy: PeriodicPolicy):
        periodic_event = create_periodic_action(id(policy))
        receive_periodic_events = partial(self._receive_periodic_events,
                                          periodic_event)
        update_wrapper(receive_periodic_events,
                       self._receive_periodic_events)
        self.policies_and_actions[policy] = receive_periodic_events
        self.clock_add_listener(receive_periodic_events,
                                predicate=lambda event, period=policy.period: event.
                                value % period == 0)

    def _receive_periodic_events(self, periodic_event: CallbackType, time_event: TimeEvent):
        self.logger.debug('Periodic event executed on %s', time_event.value)
        self.received_periodic_events.append(periodic_event)
