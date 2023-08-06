import pytest  # type: ignore

from arps.core.simulator.resource import EvtType, Resource, TrackedValue
from arps.core.simulator.resource_event import ResourceEvent
from arps.test_resources.dummies.dummy_resource import DummyCategory
from arps.test_resources.dummies.resources import ResourceA, ResourceB


def initial_resource_event(resource):
    return ResourceEvent.from_resource(resource, 0, str(None), EvtType.none)


def test_resource_event_creation():
    resource = Resource(environment_identifier=0, category=DummyCategory.Value, initial_state=10)

    resource_event = ResourceEvent.from_resource(resource=resource, epoch=0, modifier_id=0, evt_type=EvtType.none)

    assert resource_event.env == '0'
    assert resource_event.identifier == 'Resource'
    assert resource_event.epoch == '0'
    assert resource_event.value == '10'
    assert resource_event.modifier_id == '0'
    assert resource_event.type == 'none'


@pytest.mark.asyncio
async def test_listening_single_resource():
    resource = ResourceA(environment_identifier=0)

    epoch = 0

    listener_log = list()
    assert 0 == len(listener_log)
    resource.add_listener(listener_log.append)

    await resource.wait_for_notified_tasks()

    assert 1 == len(listener_log)
    assert initial_resource_event(resource) == listener_log[0]
    modified_a_id = 'a'
    modified_b_id = 'b'

    resource.value = TrackedValue(10, epoch, modified_a_id, EvtType.des_main)

    await resource.wait_for_notified_tasks()

    assert 2 == len(listener_log)
    event = ResourceEvent.from_resource(resource, 0, modified_a_id, EvtType.des_main)
    assert event == listener_log[1]

    epoch += 1

    resource.value = TrackedValue(15, epoch, modified_b_id, EvtType.des_main)

    await resource.wait_for_notified_tasks()

    assert 3 == len(listener_log)
    event = ResourceEvent.from_resource(resource, 1, modified_b_id, EvtType.des_main)
    assert event == listener_log[2]

    epoch += 1

    resource.value = TrackedValue(80, epoch, modified_a_id, EvtType.des_pos)

    await resource.wait_for_notified_tasks()

    assert 4 == len(listener_log)

    event = ResourceEvent.from_resource(resource, 2, modified_a_id, EvtType.des_pos)
    assert event == listener_log[3]


@pytest.mark.asyncio
async def test_listening_multiple_resources():
    resource_1 = ResourceA(environment_identifier=0)
    resource_2 = ResourceB(environment_identifier=0)

    modified_a_id = 'a'
    modified_b_id = 'b'

    epoch = 0

    listener_1_log = list()
    resource_1.add_listener(listener_1_log.append)

    await resource_1.wait_for_notified_tasks()

    listener_2_log = list()
    resource_2.add_listener(listener_2_log.append)

    await resource_2.wait_for_notified_tasks()

    assert resource_1.value is None
    assert resource_2.value is None

    assert initial_resource_event(resource_1) == listener_1_log[0]
    assert initial_resource_event(resource_2) == listener_2_log[0]

    resource_1.value = TrackedValue(10, epoch, modified_a_id, EvtType.des_main)
    await resource_1.wait_for_notified_tasks()
    assert 2 == len(listener_1_log)

    event = ResourceEvent.from_resource(resource_1, 0, modified_a_id, EvtType.des_main)
    assert event == listener_1_log[1]

    assert 1 == len(listener_2_log)

    resource_2.value = TrackedValue('ON', epoch, modified_b_id, EvtType.des_main)
    await resource_2.wait_for_notified_tasks()
    assert 2 == len(listener_1_log)

    event = ResourceEvent.from_resource(resource_1, 0, modified_a_id, EvtType.des_main)
    assert event == listener_1_log[1]

    assert 2 == len(listener_2_log)
    event = ResourceEvent.from_resource(resource_2, 0, modified_b_id, EvtType.des_main)
    assert event == listener_2_log[1]


@pytest.mark.asyncio
async def test_reset():
    resource = ResourceA(environment_identifier=0, initial_state=20)

    value = None

    def listener(event):
        nonlocal value
        value = event

    resource.add_listener(listener)

    await resource.wait_for_notified_tasks()

    assert initial_resource_event(resource) == value

    modified_a_id = 'a'

    resource.value = TrackedValue(10, 0, modified_a_id, EvtType.des_main)
    await resource.wait_for_notified_tasks()

    event = ResourceEvent.from_resource(resource, 0, modified_a_id, EvtType.des_main)
    assert event == value

    value = None
    resource.reset()

    assert 20 == resource.value
    resource.value = TrackedValue(10, 0, modified_a_id, EvtType.des_main)
    await resource.wait_for_notified_tasks()

    resource.add_listener(listener)
    await resource.wait_for_notified_tasks()

    resource.value = TrackedValue(10, 0, modified_a_id, EvtType.des_main)

    await resource.wait_for_notified_tasks()

    event = ResourceEvent.from_resource(resource, 0, modified_a_id, EvtType.des_main)
    assert event == value


@pytest.mark.asyncio
async def test_resource_affecting_other_resource():
    r_1 = ResourceA(environment_identifier=0, initial_state=10)
    r_2 = ResourceB(environment_identifier=0, initial_state="ON")

    # just to have an implementation of this function without breaking
    # the other tests
    r_2.available = lambda: r_2.value == 'OFF'

    r_1.affects(r_2)

    assert r_1.value == 10
    assert r_2.value == "ON"
    assert not r_2.available()

    r_1.value = TrackedValue(31, 0, 0, EvtType.des_main)

    assert r_1.value == 31
    assert r_2.value == "OFF"
    assert r_2.available()


@pytest.mark.asyncio
async def test_valid_values():
    resource = Resource(environment_identifier=0, category=DummyCategory.Value, initial_state=10)

    resource.value = TrackedValue(15, 0, 0, EvtType.none)
    assert resource.value == 15

    resource = Resource(environment_identifier=0, category=DummyCategory.Value, initial_state="B")

    resource.value = TrackedValue("A", 0, 0, EvtType.none)
    assert resource.value == "A"

    resource = Resource(environment_identifier=0, category=DummyCategory.Complex, initial_state={1: {2: 10}})
    resource.value = TrackedValue({1: {2: 30}}, 0, 0, EvtType.none)
    assert resource.value == {1: {2: 30}}

    resource.value = TrackedValue({1: 10}, 0, 0, EvtType.none)  # substitution of a dict with a value should fail
    assert resource.value == {1: {2: 30}}

    with pytest.raises(TypeError) as err:
        resource.value = TrackedValue('single value', 0, 0, EvtType.none)

    assert str(err.value) == 'Expected value in dict format since this resource is of type complex'


def test_customizable_attributes():
    resource = Resource(
        environment_identifier=0, category=DummyCategory.Complex, attributes={'some_attr': None, 'another_attr': 10}
    )

    assert resource.some_attr is None
    assert resource.another_attr == 10


def test_invalid_values():
    with pytest.raises(AssertionError):
        Resource(environment_identifier=0, initial_state=200, category=DummyCategory.Range)

    with pytest.raises(ValueError):
        resource = Resource(environment_identifier=0, category=DummyCategory.Range, initial_state=10)

        resource.value = TrackedValue(101, 0, 0, EvtType.none)

    with pytest.raises(AssertionError):
        resource = Resource(environment_identifier=0, category=DummyCategory.Togglable, initial_state="ANY")

    with pytest.raises(ValueError):
        resource = Resource(environment_identifier=0, category=DummyCategory.Togglable, initial_state="ON")

        resource.value = TrackedValue("ANY", 0, 0, EvtType.none)


if __name__ == '__main__':
    pytest.main([__file__])
