import asyncio

from arps.core.communication_layer import CommunicableEntity
from arps.core.payload_factory import (PayloadType,
                                       response_factory,
                                       Request)
from arps.core.real.rest_api_utils import random_port


class SimpleEntity(CommunicableEntity):

    def __init__(self, identifier, agents_directory_helper, comm_layer_cls):
        communication_layer = comm_layer_cls(random_port(),
                                             agents_directory_helper)
        super().__init__(identifier, communication_layer)
        self.message = asyncio.Future()

    async def receive(self, message):
        if isinstance(message, Request):
            response = response_factory(message.type,
                                        message.receiver_id,
                                        message.sender_id,
                                        message.message_id,
                                        self.fake_news_factory(message.type))
            await self.send(response, message.sender_id)

        self.message.set_result(message)

    def fake_news_factory(self, payload_type):
        if payload_type == PayloadType.info:
            sensors = ['CPU']
            actuators = ['increase_cpu_frequency', 'decrease_cpu_frequency']
            policies = ['DummyPolicy()', 'AnotherDummyPolicy()']
            related_agents = ['0.0', '0.1', '0.2']
            return (sensors, actuators, policies, related_agents)

        if payload_type is PayloadType.sensors:
            return {'SensorID': 'sensor_value'}

        if payload_type is PayloadType.actuators:
            return {'ActuatorID': 'actuator_value'}

        if payload_type in [PayloadType.policy, PayloadType.meta_agent]:
            return 'Updated successfully'

        if payload_type is PayloadType.action:
            return 'Action scheduled to be executed'

        return 'this couldnt have happened'
