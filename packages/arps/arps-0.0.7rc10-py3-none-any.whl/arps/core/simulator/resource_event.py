from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    from arps.core.simulator.resource import Resource, EvtType


@dataclass
class ResourceEvent:
    '''
    Data class that stores information when a resource is modified.
    - env: environment where the resource belongs
    - identifier: resource identifier
    - epoch: when the resource was modified
    - category: resource category
    - value: new value attributed to the resource
    - modified_id: who modified the resource
    - type: what kind of action triggered the modification of the resource
    '''
    env: str
    identifier: str
    epoch: str
    value: str
    modifier_id: Optional[str]
    type: str

    @staticmethod
    def from_resource(resource: 'Resource', epoch: int, modifier_id: Optional[str], evt_type: 'EvtType'):
        '''
        The ResourceEvent is created using attributes from a Resource instance and the event's related attributes

        Args:
        - resource: Resource instance
        - epoch: when the resource was modified
        - modifier_id: who modified the resource
        - evt_type: what kind of action triggered the modification of the resource
        '''
        return ResourceEvent(str(resource.environment_identifier), str(resource.identifier),
                             str(epoch), str(resource.value),
                             str(modifier_id), evt_type.name)
