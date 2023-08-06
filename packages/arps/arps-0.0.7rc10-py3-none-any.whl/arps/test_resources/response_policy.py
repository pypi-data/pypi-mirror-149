from typing import Tuple
from arps.core.payload_factory import Response

from arps.core.policy import ReflexPolicy, ActionType


class ResponsePolicy(ReflexPolicy):

    def __init__(self, expected_payload, *args, **kwargs):
        self.expected_payload = expected_payload
        super().__init__(*args, **kwargs)

    def _condition(self, host, event, epoch) -> bool:
        if not isinstance(event, Response):
            self.logger('Policy expecting a response')
            return False

        is_expected = event.type == self.expected_payload
        self.logger.debug('Event of type %s is expected: %s', self.expected_payload.name, is_expected)
        return is_expected

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        return (ActionType.result, event)
