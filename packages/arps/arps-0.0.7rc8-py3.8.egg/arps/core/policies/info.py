from typing import Tuple

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import PayloadType, Request, create_info_response
from arps.core.policy import ActionType, ReflexPolicy


class InfoProviderPolicy(ReflexPolicy):
    def _condition(self, host, event, epoch) -> bool:
        if not isinstance(event, Request):
            self.logger.debug('Event is not a request')
            return False

        is_info_request = event.type == PayloadType.info
        self.logger.debug('Event is info request: %s', is_info_request)
        return is_info_request

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        sender_id = event.sender_id
        receiver_id = event.receiver_id
        message_id = event.message_id
        content = create_info_response(
            receiver_id,
            sender_id,
            message_id,
            host.sensors(),
            host.actuators(),
            host.policies_executor.policies_name,
            [str(agent_id) for agent_id in host.related_agents],
            host.coordinates,
        )

        event_action = host.send(content, AgentID.from_str(sender_id))
        return (ActionType.event, event_action)
