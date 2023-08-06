import uuid
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Union

ValueType = Enum('ValueType', 'range category value complex')


ValueParser = Callable[[Any], Any]
SimpleEnumEntry = Tuple[Any, ValueType]
ComplexEnumEntry = Tuple[Any, ValueType, ValueParser]


class ResourceCategory(Enum):
    """
    Resource Category to be subclassed depending on the domain

    Enum
    - ValueType:
        - range: for values between ranges [lim,lim]. This needs to be customized
        - category: for a list of possible values
        - value: just holds any single value
        - complex: analogous to a dict. complex value types values can be modified partially
    """

    def __init__(
        self, uuid: uuid.UUID, valid_range: Any, value_type: Any, value_parser: Optional[ValueParser] = None
    ) -> None:
        """
        Initialize each category with its range and type

        Args:
        - uuid: unique identifier to make each enum unique
        - valid_range: constraint regarding the possible values that
          resource can have
        - value_type: which type better represents the value
        - value_parser: callable to return the expected value
          representation
        """

        self.valid_range = valid_range
        self.value_type = value_type
        assert isinstance(value_type, ValueType), f'got value type {value_type} expected value type {ValueType}'
        self.value_interpreter = value_parser or (lambda value: value)

    def parse(self, value):
        return self.value_interpreter(value)

    def is_valid(self, value: Any) -> bool:
        """
        Check if the value is in the correct range accordingly to its ValueType

        Args:
        - value: value to be checked
        """
        if value is None or self.value_type in (ValueType.complex, ValueType.value):
            return True

        if self.value_type is ValueType.range:
            return self.valid_range[0] <= value <= self.valid_range[1]

        if self.value_type is ValueType.category:
            return value in self.valid_range

        raise RuntimeError(f'Should not reach here: unexpectd ValueType {self.value_type}')


def create_resource_category_enum(
    enum_name: str, enum_entries: Dict[str, Union[SimpleEnumEntry, ComplexEnumEntry]]
) -> Enum:
    """This is required since it is not possible to extend enums

    Complex and Value are native value types.
    """

    native_enum_entries = {
        'Complex': (uuid.uuid1(), None, ValueType.complex),
        'Value': (uuid.uuid1(), None, ValueType.value),
    }

    if set(native_enum_entries.keys()) & set(enum_entries.keys()):
        raise ValueError(f'It is not possible to overwrite native categories: {", ".join(native_enum_entries)}')

    unique_new_enum_entries = {}
    for value_name, value_entry in enum_entries.items():
        try:
            value_range, valid_type = value_entry
            unique_new_enum_entries[value_name] = (uuid.uuid1(), value_range, valid_type)
        except ValueError:
            value_range, valid_type, value_parser = value_entry
            unique_new_enum_entries[value_name] = (uuid.uuid1(), value_range, valid_type, value_parser)

    return ResourceCategory(enum_name, {**native_enum_entries, **unique_new_enum_entries})
