from operator import attrgetter
from typing import Tuple

from arps.core.simulator.resource import (TrackedValue,
                                          EvtType,
                                          Resource)
from arps.core.resources_table import ResourcesTable, ResourcesTableError

from arps.test_resources.dummies.resources import (ResourceA,
                                                   ResourceB,
                                                   ResourceC)
from arps.test_resources.dummies.dummy_resource import DummyCategory

import pytest  # type: ignore


SetupResourcesTable = Tuple[ResourcesTable, Tuple[Resource, Resource, Resource, Resource]]


@pytest.fixture
def setup_resources_table() -> SetupResourcesTable:
    resource_one = ResourceA(environment_identifier=0)
    resource_two = ResourceB(environment_identifier=0)
    resource_three = ResourceA(environment_identifier=1)
    resource_four = ResourceC(environment_identifier=1)

    resources_table = ResourcesTable(environment_types={0: 0, 1: 1})

    resources_table.add_resource(resource_one)
    resources_table.add_resource(resource_two)
    resources_table.add_resource(resource_three)
    resources_table.add_resource(resource_four)

    return resources_table, (resource_one, resource_two,
                             resource_three, resource_four)


def test_contains_resource(setup_resources_table: SetupResourcesTable):
    resources_table, resources = setup_resources_table
    resource_one, resource_two, resource_three, resource_four = resources
    env_zero = resources_table.resources_from_environment(environment_id=0)
    env_one = resources_table.resources_from_environment(environment_id=1)
    assert resource_one.identifier in env_zero
    assert resource_two.identifier in env_zero
    assert resource_three.identifier in env_one
    assert resource_four.identifier in env_one

    assert resource_one.identifier in env_one  # since resource_one.identifier == resource_three.identifier
    assert resource_two.identifier not in env_one
    assert resource_three.identifier in env_zero  # since resource_one.identifier == resource_three.identifier
    assert resource_four.identifier not in env_zero


def test_access_resources_table_by_identifier(setup_resources_table: SetupResourcesTable):
    resources_table, resources = setup_resources_table

    resources_available = resources_table.resources_from_environment(environment_id=0)

    assert resources[0] == resources_available['ResourceA']
    assert resources[1] == resources_available['ResourceB']

    resources_available = resources_table.resources_from_environment(environment_id=1)

    assert resources[2] == resources_available['ResourceA']
    assert resources[3] == resources_available['ResourceC']


def test_iterate_over_all_resources(setup_resources_table: SetupResourcesTable):
    resources_table, resources = setup_resources_table
    assert sorted(resources_table.resources(), key=attrgetter('identifier')) == sorted(resources, key=attrgetter('identifier'))


@pytest.mark.asyncio
async def test_reset_resources(setup_resources_table: SetupResourcesTable):
    resources_table, _ = setup_resources_table
    assert all(resource.value is None for resource in resources_table.resources())
    for resource in resources_table.resources():
        if resource.category == DummyCategory.Range:
            resource.value = TrackedValue(15, 0, None, EvtType.none)
        elif resource.category == DummyCategory.Togglable:
            resource.value = TrackedValue("ON", 0, None, EvtType.none)

    assert all(resource.value is not None for resource in resources_table.resources())

    resources_table.reset()

    assert all(resource.value is None for resource in resources_table.resources())


def test_error_trying_to_insert_same_id_to_the_table(setup_resources_table: SetupResourcesTable):
    resources_table, _ = setup_resources_table

    with pytest.raises(ResourcesTableError) as excinfo:
        resource = ResourceC(environment_identifier=1)
        resources_table.add_resource(resource)

    assert 'Resource already registered' == str(excinfo.value)


def test_error_no_identifier(setup_resources_table: SetupResourcesTable):
    resources_table, _ = setup_resources_table

    with pytest.raises(IndexError) as excinfo:
        resources_available = resources_table.resources_from_environment(environment_id=1)
        resources_available['R55']  # anything but ResourceA or ResourceC

    assert 'Resource R55 not found in ResourcesTable' == str(excinfo.value)


def test_table_contains_only_added_resources(setup_resources_table: SetupResourcesTable):
    resources_table, resources = setup_resources_table
    resources_id = {resource.identifier for resource in resources}
    resources_id_from_table = set()

    for environment in resources_table.environments:
        for resource_id in environment._resources.keys():
            resources_id_from_table.add(resource_id)

    assert resources_id == resources_id_from_table


if __name__ == '__main__':
    pytest.main([__file__])
