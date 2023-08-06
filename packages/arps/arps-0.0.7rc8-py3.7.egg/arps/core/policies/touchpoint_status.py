from typing import Tuple

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (PayloadType,
                                       Request,
                                       create_touchpoint_response,
                                       parse_payload_type)
from arps.core.policy import (ActionType,
                              ReflexPolicy)

''' These classes provide an interaction to obtain touchpoint status.

If it is a sensor touchpoint, then sensors are going to be read

If it is an actuator touchpoint, then the current status of the
actuator is going to be retrieved

'''


class TouchPointStatusProviderPolicy(ReflexPolicy):
    '''
    This class creates a response containing all touchpoints loaded
    '''

    def _condition(self, host, event, epoch) -> bool:
        if not isinstance(event, Request):
            self.logger.debug('Not a Request for sensor or actuator')
            return False

        is_touchpoint = event.type in (PayloadType.sensors,
                                       PayloadType.actuators)
        self.logger.debug('Event is sensor or actuator request: %s', is_touchpoint)
        return is_touchpoint

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        self.logger.debug('Data available to perform action: host %s, event %s, and epoch %s',
                          host, event, epoch)
        sender_id = event.sender_id
        receiver_id = event.receiver_id
        message_id = event.message_id

        touchpoint_type = parse_payload_type(event.type)
        touchpoints = self._touchpoints(touchpoint_type, host)
        content = create_touchpoint_response(receiver_id,
                                             sender_id,
                                             touchpoint_type,
                                             touchpoints,
                                             message_id)
        self.logger.debug('Content generated on action: %s', content)
        event_action = host.send(content, AgentID.from_str(sender_id))
        return (ActionType.event, event_action)

    def _touchpoints(self, touchpoint_type, host):
        touchpoints = {}
        if touchpoint_type == PayloadType.sensors:
            touchpoints = {sensor: host.read_sensor(sensor) for sensor in host.sensors()}
        elif touchpoint_type == PayloadType.actuators:
            touchpoints = {actuator: host.read_actuator(actuator) for actuator in host.actuators()}

        return touchpoints
