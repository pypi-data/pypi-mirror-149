'''Just to show examples of how to create a policy

'''
from collections import namedtuple
from typing import Tuple

import pytest # type: ignore

from arps.core.agent_id_manager import AgentID
from arps.core.policy import (ReflexPolicy,
                              ActionType)
from arps.core.payload_factory import Request, Response
from arps.test_resources.dummies.dummy_policy import DummyPolicy

DUMMY_HOST = namedtuple('DUMMY_HOST', 'identifier')


@pytest.fixture
def host():
    yield DUMMY_HOST(AgentID(0, 1))


def test_basic_reflex_policy_condition_met(host):

    policy = DummyPolicy()

    request = Request(str(host.identifier),
                      str(host.identifier),
                      'dummy')

    assert (ActionType.result, request) == policy.event(host, request, 0)


def test_basic_reflex_policy_condition_not_met(host):

    policy = DummyPolicy()

    not_a_request = Response(str(host.identifier),
                             str(host.identifier),
                             'dummy')
    assert policy.event(host, not_a_request, 0) is None


def test_illformed_condition_without_parameter_reflex_policy(host):
    class IllformedReflexPolicy(ReflexPolicy):
        pass

    with pytest.raises(TypeError):
        policy = IllformedReflexPolicy()
        policy.event(host)


def test_illformed_action_reflex_policy(host):
    class IllformedReflexPolicy(ReflexPolicy):

        def _condition(self, host, event, epoch) -> bool:
            return True

        def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
            raise RuntimeError('Wasnt suppose to get here')

    with pytest.raises(TypeError):
        policy = IllformedReflexPolicy()
        not_a_request = 1  # Anything that is not a Request
        assert not policy.event(not_a_request)


if __name__ == '__main__':
    pytest.main([__file__])
