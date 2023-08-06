'''
This module contains a set of policies to use as dummy policies

DummyPolicy will always be True when a request event arrives and do nothing

DummyPolicyWithBehavior evaluate the condition using Sensors and modify Actuators when it is True

Sender and Receiver Policies are to implement a simple communication between agent.
Sender sends and Receiver increments number of messages received.
'''
from typing import Tuple

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (PayloadType,
                                       Request,
                                       Response,
                                       create_action_request,
                                       create_action_response)
from arps.core.policy import (ReflexPolicy,
                              PeriodicPolicy,
                              ActionType)
from arps.core.metrics_logger import PolicyEvaluatedMetric


class DummyPolicy(ReflexPolicy):
    '''
    Dummy policy for tests.
    '''

    def _condition(self, host, event, epoch) -> bool:
        '''
        Condition to be evaluated True when a event of type request is received
        '''
        condition = isinstance(event, Request)
        self.logger.info('Event is a request? %s', condition)
        return condition

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        '''
        Returns the request
        '''
        self.logger.info('result: %s', event)
        return (ActionType.result, event)


class DummyPeriodicPolicy(PeriodicPolicy):

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        '''
        Returns the request
        '''
        self.logger.info('result: %s', event)
        return (ActionType.result, event)


class DummyPolicyWithBehavior(PeriodicPolicy):
    '''
    Dummy policy for tests.
    '''

    def __init__(self, condition=None, action=None):
        self.condition = condition or (lambda sensor_value: sensor_value > 10)
        self.action = action or (lambda: 1)
        super().__init__()

    def _condition(self, host, event, epoch) -> bool:
        '''
        Returns True if Sensor B value met condition defined by self.condition
        '''
        periodic_payload = super()._condition(host, event, epoch)
        sensor_value = host.read_sensor('ResourceA')
        sensor_value = sensor_value if isinstance(sensor_value, int) else len(sensor_value)
        condition = periodic_payload and self.condition(sensor_value)

        self.logger.info('Condition %s met? %s', self.condition, condition)
        return condition

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        '''
        Changes Actuator A to self.action returned value if condition is met
        '''
        current_state = host.read_actuator('ResourceC')
        self.logger.info('current state of ResourceC: %s', current_state)

        try:
            self.logger.info('Action %s', self.action)
            host.modify_actuator('ResourceC', value=current_state + self.action(),
                                 identifier=host.identifier, epoch=epoch)
        except ValueError as err:
            self.logger.warning(err)

        current_state = host.read_actuator('ResourceC')
        self.logger.info('new state of ResourceC: %s', current_state)

        return (ActionType.result, True)


class DummyPolicyForSimulator(DummyPolicyWithBehavior):

    def __init__(self):
        super().__init__(condition=DummyPolicyForSimulator._greater_than_threshold,
                         action=DummyPolicyForSimulator._decrement_resource_value)

    @staticmethod
    def _greater_than_threshold(sensor_value):
        return sensor_value >= 11

    @staticmethod
    def _decrement_resource_value():
        return -1


class DefaultDummyPolicyForSimulator(DummyPolicyWithBehavior):

    def __init__(self):
        super().__init__(condition=DefaultDummyPolicyForSimulator._less_than_threshold,
                         action=DefaultDummyPolicyForSimulator._increment_resource_value)

    @staticmethod
    def _less_than_threshold(sensor_value):
        return sensor_value < 11

    @staticmethod
    def _increment_resource_value():
        return 1


class SenderPolicy(PeriodicPolicy):
    required_metrics = [PolicyEvaluatedMetric]

    def _condition(self, host, event, epoch) -> bool:
        a_periodic_action = event.type == PayloadType.periodic_action
        self.logger.info('Event is a periodic action request: %s', a_periodic_action)
        return a_periodic_action

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        async def dummy_event():
            for related_agent in host.related_agents:
                self.logger.info('Sending action to %s', related_agent)
                message = create_action_request(str(host.identifier), str(related_agent),
                                                None, event.message_id)
                try:
                    await host.send(message, related_agent)
                    self.logger.info('Event to %s created', related_agent)
                except ValueError as err:
                    self.logger.error(err)

        host.metrics_logger.update_policies_evaluated(SenderPolicy.__name__, epoch)
        return (ActionType.event, dummy_event())


class ReceiverPolicy(ReflexPolicy):
    required_metrics = [PolicyEvaluatedMetric]

    def _condition(self, host, event, epoch) -> bool:
        if not isinstance(event, Request):
            self.logger.info('Event is not an action request')
            return False

        an_action = event.type == PayloadType.action
        self.logger.info('Event is an action request: %s', an_action)
        return an_action

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        value = host.read_actuator('ReceivedMessagesResource')
        host.modify_actuator('ReceivedMessagesResource',
                             value=value + 1,
                             epoch=epoch,
                             identifier=host.identifier)
        self.logger.info('Actuator modified to %s', host.read_actuator('ReceivedMessagesResource'))
        host.metrics_logger.update_policies_evaluated(ReceiverPolicy.__name__, epoch)

        sender_id = event.receiver_id
        receiver_id = event.sender_id
        content = f'Executed action requested by {receiver_id}'
        message = create_action_response(sender_id, receiver_id,
                                         content, event.message_id)

        return (ActionType.event, host.send(message, AgentID.from_str(receiver_id)))


class CollectResponsePolicy(ReflexPolicy):

    def _condition(self, host, event, epoch) -> bool:
        return isinstance(event, Response)

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        return (ActionType.result, event)
