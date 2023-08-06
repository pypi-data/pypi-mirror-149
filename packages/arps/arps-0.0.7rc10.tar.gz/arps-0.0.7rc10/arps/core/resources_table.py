from typing import Callable, Any, Dict, Set, Iterator
from collections import abc
import warnings
import logging

from arps.core.abstract_resource import AbstractResource


class ResourcesTableError(Exception):
    '''Error raised when there is something wrong while manipulating the
    resources in the table

    '''


class Resources(abc.Collection):
    '''This class contain resources associated with an environment

    '''

    def __init__(self, environment_id: int, environment_type: int) -> None:
        self.environment_id = environment_id
        self.environment_type = environment_type
        self._resources: Dict[str, AbstractResource] = dict()

    def _add_resource_instance(self, resource_instance: AbstractResource) -> None:
        if resource_instance.identifier in self._resources:
            raise ResourcesTableError('Resource already registered')
        self._resources[resource_instance.identifier] = resource_instance

    def __getitem__(self, identifier: str) -> AbstractResource:
        '''
        Return resource by its global unique identifier

        If resource not found, raise ResourcesTableError
        '''
        if identifier not in self._resources:
            raise IndexError(f'Resource {identifier} not found in ResourcesTable')

        return self._resources[identifier]

    def __len__(self) -> int:
        return len(self._resources)

    def __iter__(self) -> Iterator[AbstractResource]:
        return iter(self._resources.values())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resources):
            return NotImplemented
        return self.environment_id == other.environment_id

    def __hash__(self):
        return hash(self.environment_id)

    def __contains__(self, identifier: object) -> bool:
        if isinstance(identifier, str):
            return identifier in self._resources

        return False


class ResourcesTable:
    '''
    Resources table organizes resources hierarchically:
    - Agent Manager Identifier (which environment the resource is part)
    -- Resources organized by their categories (which category the
       resource is classified)
    '''

    def __init__(self, environment_types: Dict[int, int]) -> None:
        '''Initialize resources table

        Args

        - environment_types: a dict containing as key the environment
        identifier and as value its type. Its purpose is to help
        differentiate the which type of event can be assigned to an
        environment.

        '''
        self.environments: Set[Resources] = set(Resources(identifier, env_type) for identifier, env_type in environment_types.items())
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_resource(self, resource_instance: AbstractResource) -> None:
        '''
        Add resource into the resources table. Resources are grouped
        by environment and category

        Args:
        - resource_instance: instance of class AbstractResource
        '''
        assert isinstance(resource_instance, AbstractResource)
        environment_id = resource_instance.environment_identifier
        try:
            resources = self.resources_from_environment(environment_id=environment_id)
        except ResourcesTableError as err:
            self.logger.warn('Error while adding resource to ResourcesTable')
            self.logger.warn(err)
        else:
            resources._add_resource_instance(resource_instance)

    def resources_from_environment(self, *, environment_id: int) -> Resources:
        '''
        Return all categories from a specific environment

        Args:
        - environment: environment identifier
        '''
        try:
            return next(resources for resources in self.environments if environment_id == resources.environment_id)
        except StopIteration:
            raise ResourcesTableError(f'Invalid environment identifier: {environment_id}')

    def add_resources_listener(self, logger: Callable[[Any], bool]):
        '''
        Invoke logger when a resource is modified

        Args:
        - logger: a function expecting a Resouce.Event as parameter to be logged
        '''
        try:
            for resource in self.resources():
                resource.add_listener(logger)
        except AttributeError:
            warnings.warn('This isn\'t supposed to be invoked in real resources')

    def remove_resources_listener(self, logger: Callable[[Any], bool]):
        '''
        Remove logger attached to each resource

        Args:
        - logger: a function expecting a Resouce.Event as parameter to be logged
        '''
        try:
            for resource in self.resources():
                resource.remove_listener(logger)
        except AttributeError:
            warnings.warn('This isn\'t supposed to be invoked in real resources')

    def reset(self):
        '''
        Reset resource state when resource is a fake resource, otherwise do nothing
        '''
        try:
            for resource in self.resources():
                resource.reset()
        except AttributeError:
            warnings.warn('This isn\'t supposed to be invoked in real resources')
            return

    def resources(self):
        '''
        Generator of all resources
        '''
        for environment in self.environments:
            for resource in environment._resources.values():
                yield resource
