import copy
import logging
from enum import Enum, auto
from typing import Any, Dict, NamedTuple, Optional

from arps.core.abstract_resource import AbstractResource
from arps.core.observable_mixin import ObservableMixin
from arps.core.resource_category import ResourceCategory, ValueType
from arps.core.simulator.resource_event import ResourceEvent


class EvtType(Enum):
    """enum that contains the actions that can trigger resource
    modification

    - des_pre: the discrete event allocate_resource from SimTask
    - des_main: the discrete event main_task from SimTask modified the
      resource
    - des_pos: the discrete event pos from SimTask modified the
      resource
    - mas: an agent modified the resource
    - rsc_indirect: another resource caused the resource to be
      modified
    - none: none of the above categories

    """

    des_pre = auto()
    des_main = auto()
    des_pos = auto()
    mas = auto()
    rsc_indirect = auto()
    none = auto()


class TrackedValue(NamedTuple):
    """
    Class to agreggate parameters of values that represents the current resource state
    and are tracked

    Params:
    - value: the new state the resource will be
    - epoch: when the resource is modified
    - modifier_id: who modified the resource
    - event_type: what kind of event caused the modification
    """

    value: Any
    epoch: int
    modifier_id: Optional[str]
    event_type: EvtType


class Resource(AbstractResource, ObservableMixin):
    """Class Resource that represents an abstraction of a fake resource
    in the environment

    Listeners can be attached to listen when the resource is modified

    A keyword parameter called init_parameter can be present in the
    initializer of the derived class.

    """

    def __init__(
        self,
        *,
        environment_identifier,
        category: ResourceCategory,
        initial_state: Optional[Any] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Args:
        - environment_identifier: environment identifier where the resource is available
        - identifier: resource unique identifier within the environment
        - category: what type of resource it is and its limits (when it is applied)
        - initial_state: initial value of the resource
        - attributes: a dict containing an attribute name and its
          value. It can be accessed as a class attribute by the
          derived class

        """
        AbstractResource.__init__(self, environment_identifier, category)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._value = initial_state
        assert self.category.is_valid(initial_state)
        self._original_value = copy.deepcopy(initial_state)
        self._affected_resource = None
        ObservableMixin.__init__(self)

        if attributes:
            for name, value in attributes.items():
                if not hasattr(self, name):
                    setattr(self, name, value)
                else:
                    self.logger.warning(f'Attribute {name} is already present and cannot be set')

    def affects(self, affected_resource):
        """
        Set resource that will be indirected affect by this resource
        """
        self._affected_resource = affected_resource

    def _affect_resource(self, epoch):
        """
        Execute process to change affected resource value.
        The behavior is dependent on each implementation

        Args:
        - epoch: when the resource was modified
        """

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, tracked_value: TrackedValue) -> None:
        """
        Change value and tracks who and when this value was changed

        Args
        - tracked_value: tuple containing value, epoch, who is modifying the value respectively,
        and what kind of event modified the resource
        """
        value, epoch, modifier_id, evt_type = tracked_value
        if not self.category.is_valid(value):
            message = f'Value type expected {self.category.value_type.name} in range {str(self.category.valid_range)}'
            raise ValueError(message)

        self.logger.debug('Setting new resource state to %s', value)

        if self.category.value_type is ValueType.complex and not isinstance(value, dict):
            raise TypeError('Expected value in dict format since this resource is of type complex')

        def recursive_set(current_value_level, value):
            for k, v in value.items():
                if isinstance(v, dict):
                    recursive_set(current_value_level[k], v)
                else:
                    # only modifies existing keys; don't overwrite dict values with single values
                    if k in current_value_level and not isinstance(current_value_level[k], dict):
                        current_value_level[k] = v

        # When resource is complex, we just set its partial value
        if self.category.value_type is ValueType.complex and self._value is not None:
            recursive_set(self._value, value)
        else:
            self._value = value

        assert isinstance(evt_type, EvtType)

        self.logger.debug('Notify resource modification')
        event = ResourceEvent.from_resource(self, epoch, modifier_id, evt_type)
        self.notify(event)

        self.logger.debug('Notify affected resource')
        self._affect_resource(epoch)

    def add_listener(self, listen, predicate=None):
        super().add_listener(listen, predicate=lambda event: event.identifier == self.identifier)
        event = ResourceEvent.from_resource(self, 0, str(None), EvtType.none)
        self.notify(event)

    def reset(self):
        """
        Set the resource to its original value
        Remove all listeners
        """
        self._value = self._original_value
        super().clear()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name}(id={self.identifier}, env={self.environment_identifier}, initial_state={self.value})'

    def available(self) -> bool:
        """Derived class must implement this if the resource is limited"""
        return True
