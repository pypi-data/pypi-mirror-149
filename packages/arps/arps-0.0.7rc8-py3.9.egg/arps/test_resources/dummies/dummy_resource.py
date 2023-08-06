from arps.core.abstract_resource import AbstractResource
from arps.core.resource_category import ValueType, create_resource_category_enum
from arps.core.simulator.resource import EvtType, Resource, TrackedValue


class RealResource(AbstractResource):
    def __init__(self, *, environment_identifier, initial_state=None, category):
        super().__init__(environment_identifier=environment_identifier, category=DummyCategory.Range)
        self._value = initial_state

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


DummyCategory = create_resource_category_enum(
    'DummyCategory',
    {
        'Range': ((0, 100), ValueType.range),
        'Togglable': (('ON', 'OFF'), ValueType.category),
        'Counter': ((0, float('inf')), ValueType.range),
    },
)


class DummyRealResource(RealResource):
    def __init__(self, *, environment_identifier):
        super().__init__(
            environment_identifier=environment_identifier, initial_state='RealResource', category=DummyCategory.Value
        )


class DummyFakeResource(Resource):
    def __init__(self, *, environment_identifier):
        super().__init__(
            environment_identifier=environment_identifier, initial_state='FakeResource', category=DummyCategory.Value
        )


class DummyRealComplexResource(RealResource):
    def __init__(self, *, environment_identifier):
        super().__init__(environment_identifier=environment_identifier, category=DummyCategory.Complex)


class DummyFakeComplexResource(Resource):
    def __init__(self, *, environment_identifier):
        super().__init__(environment_identifier=environment_identifier, category=DummyCategory.Complex)


class FakeResourceA(Resource):
    def __init__(self, *, environment_identifier, initial_state=None, attributes=None):
        super().__init__(
            environment_identifier=environment_identifier,
            initial_state=initial_state,
            category=DummyCategory.Range,
            attributes=attributes,
        )

    def _affect_resource(self, epoch):
        if not self._affected_resource:
            return

        new_value = 'ON' if self.value > 60 else 'OFF'
        if self._affected_resource.value == new_value:
            return

        self._affected_resource.value = TrackedValue(new_value, epoch, self.identifier, EvtType.rsc_indirect)


class FakeResourceB(Resource):
    def __init__(self, *, environment_identifier, initial_state=None, attributes=None):
        super().__init__(
            environment_identifier=environment_identifier,
            initial_state=initial_state,
            category=DummyCategory.Togglable,
            attributes=attributes,
        )


class FakeResourceC(Resource):
    def __init__(self, *, environment_identifier, initial_state=None, attributes=None):
        super().__init__(
            environment_identifier=environment_identifier,
            initial_state=initial_state,
            category=DummyCategory.Range,
            attributes=attributes,
        )


class FakeReceivedMessagesResource(Resource):
    def __init__(self, *, environment_identifier):
        super().__init__(environment_identifier=environment_identifier, initial_state=0, category=DummyCategory.Counter)
