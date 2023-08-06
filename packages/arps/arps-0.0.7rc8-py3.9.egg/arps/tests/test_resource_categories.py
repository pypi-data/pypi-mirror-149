import pytest

from arps.core.resource_category import ValueType, create_resource_category_enum


def test_extend_resource_category_enum():
    ExtendedResourceCategory = create_resource_category_enum(
        'ExtendedResourceCategory', {'A': (None, ValueType.complex), 'B': ((0, 10), ValueType.range)}
    )

    assert set(['Complex', 'Value', 'A', 'B']) == set([enum_entry.name for enum_entry in ExtendedResourceCategory])


def test_extend_resource_category_enum_failure():

    with pytest.raises(ValueError) as err:
        create_resource_category_enum(
            'ExtendedResourceCategory', {'A': (None, ValueType.complex), 'Complex': ((0, 10), ValueType.range)}
        )
    assert str(err.value) == 'It is not possible to overwrite native categories: Complex, Value'


def test_if_is_valid():
    ExtendedResourceCategory = create_resource_category_enum(
        'ExtendedResourceCategory',
        {'Range': ((0, 10), ValueType.range), 'Category': (('A', 'B', 'C'), ValueType.category)},
    )

    assert set(['Complex', 'Value', 'Range', 'Category']) == set(
        [enum_entry.name for enum_entry in ExtendedResourceCategory]
    )

    range_entry = ExtendedResourceCategory.Range
    assert range_entry.is_valid(5)
    assert not range_entry.is_valid(11)

    range_entry = ExtendedResourceCategory.Category
    assert range_entry.is_valid('A')
    assert range_entry.is_valid('B')
    assert range_entry.is_valid('C')
    assert not range_entry.is_valid('D')


def test_parse():
    ExtendedResourceCategory = create_resource_category_enum(
        'ExtendedResourceCategory', {'Range': ((0, 10), ValueType.range, lambda v: str(v))}
    )

    assert set(['Complex', 'Value', 'Range']) == set([enum_entry.name for enum_entry in ExtendedResourceCategory])

    range_entry = ExtendedResourceCategory.Range
    assert range_entry.parse(5) == '5'
