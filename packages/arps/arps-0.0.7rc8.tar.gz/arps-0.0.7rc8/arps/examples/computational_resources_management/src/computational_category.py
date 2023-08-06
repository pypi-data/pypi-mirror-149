import uuid

from arps.core.resource_category import ResourceCategory, ValueType


class ComputationalCategory(ResourceCategory):
    CPU = (uuid.uuid1(), (0, 100), ValueType.int)
    CPUFreq = (uuid.uuid1(), None, ValueType.complex)
    Energy = (uuid.uuid1(), (0, 50), ValueType.float)
