import pytest # type: ignore

from arps.core.touchpoint import Sensor, Actuator
from arps.core.environment import Environment
from arps.test_resources.dummies.resources import ResourceA, ResourceB
from arps.test_resources.dummies.dummy_policy import (DummyPolicy,
                                                      DummyPeriodicPolicy,
                                                      DummyPolicyWithBehavior)


def test_environment_creation():

    resource_a = ResourceA(environment_identifier=0)
    resource_b = ResourceB(environment_identifier=0)
    sensor_a = Sensor(resource_a)
    sensor_b = Sensor(resource_b)
    actuator_b = Actuator(resource_b)

    environment = Environment(sensors=[sensor_a, sensor_b],
                              actuators=[actuator_b])

    assert sensor_a == environment.sensor('ResourceA')
    assert sensor_b == environment.sensor('ResourceB')
    assert actuator_b == environment.actuator('ResourceB')


def test_get_environment_resource():
    resource_a = ResourceA(environment_identifier=0)
    resource_b = ResourceB(environment_identifier=0)
    environment = Environment(sensors=[Sensor(resource=resource_a),
                                       Sensor(resource=resource_b)],
                              actuators=[Actuator(resource=resource_b)])

    environment_resource = environment.resources()
    assert resource_a == environment_resource['ResourceA']
    assert resource_b == environment_resource['ResourceB']


def test_constraint_of_shared_resources():
    resource_a = ResourceA(environment_identifier=0)

    with pytest.raises(ValueError) as excinfo:
        Environment(sensors=[Sensor(resource=resource_a),
                             Sensor(resource=resource_a)],
                    actuators=[])

    assert str(excinfo.value) == 'Resources instances cannot be shared among sensors.'

    with pytest.raises(ValueError) as excinfo:
        Environment(actuators=[Actuator(resource=resource_a),
                               Actuator(resource=resource_a)],
                    sensors=[])

    assert str(excinfo.value) == 'Resources instances cannot be shared among actuators.'

    # among a sensor and an actuator is fine
    environment = Environment(actuators=[Actuator(resource=resource_a)],
                              sensors=[Sensor(resource=resource_a)])
    environment_resource = environment.resources()
    assert resource_a == environment_resource['ResourceA']


@pytest.fixture
def environment():
    # No touchpoints or resources are required
    environment = Environment(sensors=[], actuators=[])
    for policy in environment.list_registered_policies():
        environment.unregister_policy(policy)
    environment.register_policy(DummyPolicy.__name__, DummyPolicy)
    environment.register_policy(DummyPeriodicPolicy.__name__, DummyPeriodicPolicy)

    yield environment

    environment.unregister_policy(DummyPolicy.__name__)
    environment.unregister_policy(DummyPeriodicPolicy.__name__)


def test_registered_policies(environment):
    policies = environment.list_registered_policies()
    assert [DummyPolicy.__name__, DummyPeriodicPolicy.__name__] == policies, policies

    environment.register_policy(DummyPolicyWithBehavior.__name__, DummyPolicyWithBehavior)
    assert sorted([DummyPolicy.__name__, DummyPeriodicPolicy.__name__, DummyPolicyWithBehavior.__name__]) == sorted(environment.list_registered_policies())

    environment.unregister_policy(DummyPolicyWithBehavior.__name__)
    assert [DummyPolicy.__name__, DummyPeriodicPolicy.__name__] == environment.list_registered_policies()


def test_load_regular_policy(environment):
    dummy_policy = environment.load_policy('DummyPolicy')
    assert dummy_policy
    assert not hasattr(dummy_policy, 'period')


def test_load_regular_policy_with_period_as_None(environment):
    dummy_policy = environment.load_policy('DummyPolicy', None)
    assert dummy_policy
    assert not hasattr(dummy_policy, 'period')


def test_load_periodic_policy(environment):
    periodic_policy = environment.load_policy('DummyPeriodicPolicy', 10)
    assert periodic_policy
    assert periodic_policy.period == 10


def test_new_policy_instance(environment):
    dummy_policy = environment.load_policy('DummyPolicy')
    another_dummy_policy = environment.load_policy('DummyPolicy')

    assert dummy_policy != another_dummy_policy


def test_load_periodic_policy_without_period(environment):
    with pytest.raises(ValueError) as excinfo:
        environment.load_policy('DummyPeriodicPolicy')
    assert str(excinfo.value) == 'Expected positive int period when creating periodic policy DummyPeriodicPolicy'


def test_load_periodic_policy_with_negative_period(environment):
    with pytest.raises(ValueError) as excinfo:
        environment.load_policy('DummyPeriodicPolicy', -10)
    assert str(excinfo.value) == 'Expected positive int period when creating periodic policy DummyPeriodicPolicy'


def test_load_periodic_policy_with_invalid_period(environment):
    with pytest.raises(ValueError) as excinfo:
        environment.load_policy('DummyPeriodicPolicy', 'banana')
    assert str(excinfo.value) == 'Expected positive int period when creating periodic policy DummyPeriodicPolicy'


def test_load_regular_policy_with_invalid_period(environment):
    with pytest.raises(ValueError) as excinfo:
        environment.load_policy('DummyPolicy', 'banana')
    assert str(excinfo.value) == 'Trying to use period with a non periodic policy DummyPolicy'


def test_load_regular_policy_with_valid_period(environment):
    with pytest.raises(ValueError) as excinfo:
        environment.load_policy('DummyPolicy', 10)
    assert str(excinfo.value) == 'Trying to use period with a non periodic policy DummyPolicy'


def test_policy_is_registered(environment):

    assert environment.is_policy_registered('DummyPolicy')

    assert not environment.is_policy_registered('SomeDummyPolicyNotRegistered')





if __name__ == '__main__':
    pytest.main([__file__])
