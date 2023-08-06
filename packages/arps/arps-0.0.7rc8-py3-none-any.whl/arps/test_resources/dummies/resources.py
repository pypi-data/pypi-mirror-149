from arps.core import create_resource_class, select_resource_class

from .dummy_resource import (
    DummyFakeComplexResource,
    DummyFakeResource,
    DummyRealComplexResource,
    DummyRealResource,
    FakeReceivedMessagesResource,
    FakeResourceA,
    FakeResourceB,
    FakeResourceC,
)

DummyResource = select_resource_class('DummyResource', DummyFakeResource, DummyRealResource)

DummyComplexResource = select_resource_class('DummyComplexResource', DummyFakeComplexResource, DummyRealComplexResource)

ResourceA = create_resource_class('ResourceA', FakeResourceA)

ResourceB = create_resource_class('ResourceB', FakeResourceB)

ResourceC = create_resource_class('ResourceC', FakeResourceC)

ReceivedMessagesResource = create_resource_class('ReceivedMessagesResource', FakeReceivedMessagesResource)
