from collections import namedtuple

from arps.core.mobile_entity import Coordinates
from arps.core.simulator.resource import Resource
from arps.test_resources.dummies.dummy_resource import DummyCategory

CoordinateEntry = namedtuple('CoordinateEntry', 'origin target')


class MobileResources(Resource):

    coordinate_entries = [
        CoordinateEntry(Coordinates(4, 4, 0), Coordinates(8, 7, 1)),
        CoordinateEntry(Coordinates(3, 3, 2), Coordinates(9, 1, 3)),
    ]

    def generate_coordinates(self):
        return {
            index: {
                "coordinates": coordinate_entry.origin,
                "owner": None,
                "active": True,
                "target_coordinates": coordinate_entry.target,
            }
            for index, coordinate_entry in enumerate(self.coordinate_entries)
        }

    def __init__(self, *, environment_identifier):
        super().__init__(
            environment_identifier=environment_identifier,
            initial_state=self.generate_coordinates(),
            category=DummyCategory.Complex,
            attributes=None,
        )
