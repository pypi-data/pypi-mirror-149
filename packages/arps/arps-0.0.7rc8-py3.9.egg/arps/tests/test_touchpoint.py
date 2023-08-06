import pytest  # type: ignore

from arps.core.simulator.resource import EvtType, TrackedValue
from arps.core.touchpoint import Actuator, Sensor
from arps.test_resources.dummies.resources import DummyComplexResource, ResourceA


def test_touchpoint_creation_success():
    dummy_resouce = ResourceA(environment_identifier=0)
    touchpoint = Sensor(resource=dummy_resouce)

    assert touchpoint.resource_name == 'ResourceA'
    assert dummy_resouce == touchpoint.resource


def test_sensor():
    dummy_resouce = DummyComplexResource(environment_identifier=0)
    dummy_resouce.value = TrackedValue({'A': 10, 'B': 20}, 0, None, EvtType.mas)
    sensor = Sensor(resource=dummy_resouce)
    assert sensor.read() == {'A': 10, 'B': 20}  # always return just the values


def test_actuator_modify_existing_key():
    dummy_resouce = DummyComplexResource(environment_identifier=0)
    dummy_resouce.value = TrackedValue({'A': 10, 'B': 20, 'C': {'D': 30}}, 0, None, EvtType.mas)
    actuator = Actuator(resource=dummy_resouce)
    assert actuator.read() == {'A': 10, 'B': 20, 'C': {'D': 30}}  # always return just the values

    actuator.set(value={'B': 30}, epoch=1, identifier='0.0')  # Modify partially

    assert actuator.read() == {'A': 10, 'B': 30, 'C': {'D': 30}}

    actuator.set(value={'C': {'D': 40}}, epoch=2, identifier='0.0')  # Modify partially

    assert actuator.read() == {'A': 10, 'B': 30, 'C': {'D': 40}}


def test_actuator_modify_non_existing_key():
    dummy_resouce = DummyComplexResource(environment_identifier=0)
    dummy_resouce.value = TrackedValue({'A': 10, 'B': 20}, 0, None, EvtType.mas)
    actuator = Actuator(resource=dummy_resouce)
    assert actuator.read() == {'A': 10, 'B': 20}  # always return just the values

    actuator.set(value={'C': 30}, epoch=1, identifier='0.0')  # Modify partially

    assert actuator.read() == {'A': 10, 'B': 20}


if __name__ == '__main__':
    pytest.main([__file__])
