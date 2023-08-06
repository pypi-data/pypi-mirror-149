from arps.core.mobile_entity import Axis, Boundaries, Coordinates, MobileEntity


def test_coordinates_operations():
    coordinate = Coordinates(1, 1, 1)

    assert Coordinates(2, 2, 2) == (coordinate + coordinate)
    assert Coordinates(0, 0, 0) == (coordinate - coordinate)

    coordinate += Coordinates(10, 10, 10)
    assert coordinate == Coordinates(11, 11, 11)


def test_boundary():
    boundaries = Boundaries(upper=Coordinates(10, 10, 10), lower=Coordinates(0, 0, 0))

    assert boundaries.is_bounded(Coordinates(1, 1, 1))


def test_boundary_with_negative_values():
    boundaries = Boundaries(upper=Coordinates(10, -1, 18), lower=Coordinates(0, -5, 3))

    assert boundaries.is_bounded(Coordinates(1, -2, 5))


def test_boundary_limits():
    boundaries = Boundaries(upper=Coordinates(10, 10, 10), lower=Coordinates(0, 0, 0))

    assert boundaries.is_bounded(Coordinates(0, 0, 0))
    assert boundaries.is_bounded(Coordinates(10, 10, 10))


def test_out_of_bounds():
    boundaries = Boundaries(upper=Coordinates(10, 10, 10), lower=Coordinates(0, 0, 0))

    assert not boundaries.is_bounded(Coordinates(11, 0, 0))


def test_mobile_entity():
    boundaries = Boundaries(upper=Coordinates(10, 10, 10), lower=Coordinates(0, 0, 0))
    mobile_entity = MobileEntity(boundaries)
    assert mobile_entity.coordinates == Coordinates(0, 0, 0)

    mobile_entity.move(20, axis=Axis.X)

    # since the amount is out of bounds the entity remains in the same place
    assert mobile_entity.coordinates == Coordinates(0, 0, 0)

    mobile_entity.move(10, axis=Axis.X)
    mobile_entity.move(5, axis=Axis.Y)
    mobile_entity.move(3, axis=Axis.Z)

    assert mobile_entity.coordinates == Coordinates(10, 5, 3)
