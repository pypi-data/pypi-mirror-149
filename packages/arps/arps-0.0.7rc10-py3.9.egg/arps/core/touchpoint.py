import logging
from typing import Any

from arps.core.abstract_resource import AbstractResource
from arps.core.simulator.resource import EvtType, TrackedValue


class TouchPoint:
    """
    Base class that represents a touchpoint

    It offers a method to read the current touchpoint's state
    """

    def __init__(self, resource: AbstractResource):
        """
        Initializes the class setting its resource

        Args:
        - resource: resource to be read or set
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self._resource = resource
        self.logger.debug('TouchPoint created, type: %s', self.resource_name)

    def read(self):
        """
        Returns the content of the touchpoint
        Do not assume any format, it can be str or a dict for example
        """
        return self._resource.value

    @property
    def resource(self):
        return self._resource

    @property
    def resource_name(self):
        return self._resource.__class__.__name__

    def __repr__(self):
        return f'{self.__class__.__name__}({self.resource})'


class Sensor(TouchPoint):
    """
    Base class for sensor
    """


class Actuator(TouchPoint):
    """
    Base class for actuator
    """

    def set(self, *, value: Any, epoch: int, identifier: str) -> None:
        """
        Modifies the actuator state

        Args:
        - value: the value of the resource
        - epoch: when the resource is modified
        - identifier: which entity is modifying
        """

        tracked_value = TrackedValue(value, epoch, identifier, EvtType.mas)
        self._set(tracked_value)

    def _set(self, tracked_value: TrackedValue) -> None:
        """
        Just set the current resource state

        This method can be inherited if more elaborated assignment need be done
        """
        self.resource.value = tracked_value
