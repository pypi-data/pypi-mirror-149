"""This module contains a represetation of a 3D spatial location

"""

from enum import Enum
from typing import NamedTuple, Optional

import numpy as np

Axis = Enum('Axis', names='X Y Z')


class Coordinates:
    def __init__(self, x: int, y: int, z: int):
        self.data = np.array([x, y, z])

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    def __eq__(self, other: object):
        if not isinstance(other, Coordinates):
            return NotImplemented

        return all(self.data == other.data)

    def __add__(self, other: object):
        if not isinstance(other, Coordinates):
            raise TypeError(f"unsupported operand types for +: 'Coordinates' and {type(other)}")

        return Coordinates(*(self.data + other.data))

    def __sub__(self, other: object):
        if not isinstance(other, Coordinates):
            raise TypeError(f"unsupported operand types for +: 'Coordinates' and {type(other)}")

        return Coordinates(*(self.data - other.data))

    def __str__(self):
        return f'Coordinates(x={self.data[0]}, y={self.data[1]}, z={self.data[2]})'

    def __repr__(self):
        return f'Coordinates(x={self.data[0]}, y={self.data[1]}, z={self.data[2]})'


class Boundaries(NamedTuple):
    upper: Coordinates
    lower: Coordinates

    def is_bounded(self, coordinates: Coordinates):
        return all(self.lower.data <= coordinates.data) and all(coordinates.data <= self.upper.data)

    def __str__(self):
        return f'Boundaries(upper={self.upper}, lower={self.lower})'


class MobileEntity:
    """This class adds mobility features to the agents.

    If no boundaries is passed as parameter, this class does
    nothing. This was done this way because not all agents are
    mobile. Not the best way, but this is how it is going to work for
    now.

    """

    def __init__(self, boundaries: Optional[Boundaries] = None):
        self._coordinates = boundaries.lower if boundaries else None
        self.boundaries = boundaries

    @property
    def coordinates(self) -> Optional[Coordinates]:
        if self.boundaries is None:
            return None

        return self._coordinates

    @coordinates.setter
    def coordinates(self, new_coordinates: Coordinates):
        if self.boundaries is not None:
            self._coordinates = new_coordinates

    def move(self, amount: int, *, axis: Axis = Axis.X) -> None:
        """Move a certain amount in a specific axis."""

        if self.boundaries is None or self.coordinates is None:
            return

        amount = int(amount)
        amount_coordinates = MobileEntity._coordinate(amount, axis)
        if self.boundaries.is_bounded(self.coordinates + amount_coordinates):
            self.coordinates += amount_coordinates

    @staticmethod
    def _coordinate(amount: int, axis: Axis = Axis.X) -> Coordinates:
        if axis is Axis.X:
            return Coordinates(amount, 0, 0)
        elif axis is Axis.Y:
            return Coordinates(0, amount, 0)
        elif axis is Axis.Z:
            return Coordinates(0, 0, amount)
        else:
            return Coordinates(0, 0, 0)
