import pytest # type: ignore

from arps.core.simulator.estimators_table import EstimatorsTable, EstimatorsTableError


def f_one(some_value):
    return 1 + 2 * some_value


def f_two(some_value):
    return 1 + 5 * some_value


def f_three(some_value):
    return 1 + 10 * some_value


@pytest.fixture
def estimators_table():
    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'one', f_one)
    estimators_table.add_estimator(0, 'two', f_two)
    estimators_table.add_estimator(1, 'three', f_three)
    return estimators_table


def test_estimators_table(estimators_table):
    assert estimators_table[0].one(10) == 21
    assert estimators_table[0].two(10) == 51
    assert estimators_table[1].three(10) == 101


def test_estimators_table_fail(estimators_table):

    with pytest.raises(EstimatorsTableError) as excinfo:
        estimators_table.add_estimator(0, 'one', f_two)
        assert str(excinfo.value) == "'Estimator already registered for environment 0"

    with pytest.raises(EstimatorsTableError) as excinfo:
        estimators_table[2]
        assert str(excinfo.value) == 'Invalid environment'

    with pytest.raises(AttributeError) as excinfo:
        estimators_table[0].three
        assert str(excinfo.value) == "'Estimator' object has no attribute three"

if __name__ == '__main__':
    pytest.main([__file__])
