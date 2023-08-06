import abc
from typing import Any

from arps.core.resource_category import ResourceCategory


class AbstractResource(metaclass=abc.ABCMeta):

    def __init__(self, environment_identifier, category: ResourceCategory) -> None:
        '''
        Args:
        - environment_identifier: environment identifier where the resource is available
        - identifier: resource unique identifier within the environment
        - category: what type of resource it is
        '''
        self.environment_identifier = environment_identifier
        self.category = category

    @property
    @abc.abstractmethod
    def value(self) -> Any:
        '''Retrieve the internal state of the resource

        '''

    @property
    def identifier(self):
        return self.__class__.__name__
