from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, auto, unique
from functools import singledispatch
from typing import Any, Dict, List, Optional, Tuple, Union


@unique
class PayloadType(IntEnum):
    """Payload type to classify messages

    Payloads that will have a request and response

        * info - related to request/response info about the agent
        * sensors - related to request/response sensors values about
          the agent
        * actuators - related to request/response actuators values
          about the agent
        * policy - related to request/response on changing agents
          policies
        * meta_agent - related to request/response on changing agents
          related to other agents

    Payloads that will have an action to be executed

        * periodic_action - related to messages that execute periodically
        * action - related to messages that execute only once. The
          payload can be anything.

    Control related type:

       * error - contains a message describing an error that occurred
    after receiving a request

    """

    info = auto()
    sensors = auto()
    actuators = auto()
    policy = auto()
    meta_agent = auto()
    periodic_action = auto()
    action = auto()
    error = auto()


@dataclass
class BasePayload:
    sender_id: str
    receiver_id: str
    type: PayloadType
    message_id: Any = field(default=None)
    content: Any = field(default=None)

    def __eq__(self, other):
        return (
            self.message_id == other.message_id
            and self.type == other.type
            and self.content == other.content
            and self.sender_id == other.sender_id
            and self.receiver_id == other.receiver_id
        )

    def __hash__(self):
        return (
            hash(self.message_id)
            ^ hash(self.type)
            ^ hash(self.content)
            ^ hash(self.sender_id)
            ^ hash(self.receiver_id)
        )


class Request(BasePayload):
    """Payload of Request Type"""


class Response(BasePayload):
    """Payload of Response Type"""


@dataclass
class Info:
    sensors: List[str]
    actuators: List[str]
    policies: List[str]
    related_agents: List[str]

    def __eq__(self, other):
        return (
            self.sensors == other.sensors
            and self.actuators == other.actuators
            and self.policies == other.policies
            and self.related_agents == other.related_agents
        )

    def __hash__(self):
        return (
            hash(self.sensors)
            ^ hash(self.actuators)
            ^ hash(self.policies)
            ^ hash(self.related_agents)
        )


@dataclass
class SpatialInfo(Info):
    coordinates: Optional[Tuple[int, int, int]] = None


@dataclass
class TouchPoint:
    touchpoint: Dict[str, Union[str, int]]

    def __eq__(self, other):
        return self.touchpoint == other.touchpoint

    def __hash__(self):
        return hash(self.touchpoint)


@dataclass
class Meta:
    """This class has the purpose of describing a operation (MetaOP) that
    will take place in the agent. The MetaOP to be executed is described
    in the meta field

    """

    op: MetaOp
    meta: Any

    def __eq__(self, other):
        return self.op == other.op and self.meta == other.meta

    def __hash__(self):
        return hash(self.op) and hash(self.meta)


class MetaOp(IntEnum):
    add = 0
    remove = 1


@dataclass
class Status:
    status: str

    def __eq__(self, other):
        return self.status == other.status

    def __hash__(self):
        return hash(self.status)


@dataclass
class Action:
    action: str


Payload = Union[Request, Response]


def create_info_request(sender_id: str, receiver_id: str, message_id: Any) -> Request:
    return Request(sender_id, receiver_id, PayloadType.info, message_id)


def create_info_response(
    sender_id: str,
    receiver_id: str,
    message_id: Any,
    sensors: List[str],
    actuators: List[str],
    policies: List[str],
    related_agents: List[str],
    coordinates: Optional[Tuple[int, int, int]] = None,
) -> Response:
    if coordinates is None:
        info = Info(sensors, actuators, policies, related_agents)
    else:
        info = SpatialInfo(sensors, actuators, policies, related_agents, coordinates)

    return Response(sender_id, receiver_id, PayloadType.info, message_id, info)


def create_touchpoint_request(
    sender_id: str, receiver_id: str, touchpoint_type, message_id
) -> Request:
    assert touchpoint_type in (PayloadType.sensors, PayloadType.actuators)
    return Request(sender_id, receiver_id, touchpoint_type, message_id)


def create_touchpoint_response(
    sender_id: str, receiver_id: str, touchpoint_type, touchpoint, message_id: Any
) -> Response:
    assert touchpoint_type in (PayloadType.sensors, PayloadType.actuators)
    assert isinstance(touchpoint, dict)
    return Response(
        sender_id, receiver_id, touchpoint_type, message_id, TouchPoint(touchpoint)
    )


def create_policy_request(
    sender_id: str,
    receiver_id: str,
    operation,
    policy_name: Dict[str, Union[str, int]],
    message_id: Any,
) -> Request:
    return create_meta_request(
        sender_id, receiver_id, PayloadType.policy, operation, policy_name, message_id
    )


def create_policy_response(
    sender_id: str, receiver_id: str, response_content, message_id: Any
) -> Response:
    return create_meta_response(
        sender_id, receiver_id, PayloadType.policy, response_content, message_id
    )


def create_meta_agent_request(
    sender_id: str, receiver_id: str, operation, agents_id, message_id: Any
) -> Request:
    return create_meta_request(
        sender_id, receiver_id, PayloadType.meta_agent, operation, agents_id, message_id
    )


def create_meta_agent_response(
    sender_id: str, receiver_id: str, response_content, message_id: Any
) -> Response:
    return create_meta_response(
        sender_id, receiver_id, PayloadType.meta_agent, response_content, message_id
    )


def create_meta_request(
    sender_id: str, receiver_id: str, meta_type, operation, parameters, message_id: Any
) -> Request:
    assert meta_type in (PayloadType.meta_agent, PayloadType.policy)
    return Request(
        sender_id, receiver_id, meta_type, message_id, Meta(operation, parameters)
    )


def create_meta_response(
    sender_id: str, receiver_id: str, meta_type, response_content, message_id: Any
) -> Response:
    assert meta_type in (PayloadType.meta_agent, PayloadType.policy)
    return Response(
        sender_id, receiver_id, meta_type, message_id, Status(response_content)
    )


def create_action_request(
    sender_id: str, receiver_id: str, action: Any, message_id: Optional[Any] = None
) -> Request:
    """message_id is optional because sometimes the agent does not
    respond, it just perform the requested action

    """
    return Request(
        sender_id, receiver_id, PayloadType.action, message_id, Action(action)
    )


def create_action_response(
    sender_id: str, receiver_id: str, action, message_id: Any
) -> Response:
    return Response(
        sender_id, receiver_id, PayloadType.action, message_id, Status(action)
    )


def create_error_response(
    sender_id: str, receiver_id: str, message_id: Any, error_message
) -> Response:
    return Response(
        sender_id, receiver_id, PayloadType.error, message_id, error_message
    )


def create_periodic_action(policy_id: int) -> BasePayload:
    """internal periodic action associated with a specific policy.

    There is no need to associate with a sender / receiver
    """
    return BasePayload(
        sender_id=str(None),
        receiver_id=str(None),
        type=PayloadType.periodic_action,
        content=policy_id,
    )


def request_factory(
    payload_type: PayloadType,
    sender_id: str,
    receiver_id: str,
    message_id: Any,
    content: Optional[Any] = None,
):
    """Create request payload accordingly to the payload_type argument

    Args:
    - payload_type: instance of PayloadType
    - sender_id: Sender's AgentID
    - receiver_id: Receiver's AgentID
    - message_id: message id
    - content: payload_type dependent argument

    """
    if payload_type == PayloadType.info:
        return create_info_request(sender_id, receiver_id, message_id)
    elif payload_type in (PayloadType.sensors, PayloadType.actuators):
        return create_touchpoint_request(
            sender_id, receiver_id, payload_type, message_id
        )
    elif payload_type == PayloadType.policy and content:
        operation = content['operation']
        try:
            policy_name = {'policy': content['policy'], 'period': content['period']}
        except KeyError:
            policy_name = {'policy': content['policy']}

        return create_policy_request(
            sender_id, receiver_id, MetaOp[operation], policy_name, message_id
        )
    elif payload_type == PayloadType.meta_agent and content:
        operation = content['operation']
        to_agent = content['to_agent']
        return create_meta_agent_request(
            sender_id, receiver_id, MetaOp[operation], to_agent, message_id
        )
    elif payload_type == PayloadType.action:
        return create_action_request(sender_id, receiver_id, content, message_id)
    else:
        raise ValueError('Unexpected payload type or missing required content')


def response_factory(
    payload_type: PayloadType,
    sender_id: str,
    receiver_id: str,
    message_id: Any,
    content: Any,
):
    """Create response payload accordingly to the payload_type argument

    Args:
    - payload_type: instance of PayloadType
    - sender_id: Sender's AgentID in str format
    - receiver_id: Receiver's AgentID in str format
    - message_id: message id
      communication is asynchronouts
    - content: payload_type dependent argument

    """
    if payload_type == PayloadType.info:
        sensors, actuators, policies, related_agents = content
        return create_info_response(
            sender_id,
            receiver_id,
            message_id,
            sensors,
            actuators,
            policies,
            related_agents,
        )
    elif payload_type in (PayloadType.sensors, PayloadType.actuators):
        return create_touchpoint_response(
            sender_id, receiver_id, payload_type, content, message_id
        )
    elif payload_type == PayloadType.policy:
        return create_policy_response(sender_id, receiver_id, content, message_id)
    elif payload_type == PayloadType.meta_agent:
        return create_meta_agent_response(sender_id, receiver_id, content, message_id)
    elif payload_type == PayloadType.action:
        return create_action_response(sender_id, receiver_id, content, message_id)
    elif payload_type == PayloadType.error:
        return create_error_response(sender_id, receiver_id, message_id, content)
    else:
        raise ValueError(
            f'Could not create response: unexpected payload type {payload_type}'
        )


@singledispatch
def parse_payload_type(payload_type: Union[str, int]) -> PayloadType:
    """
    Arguments:
    - payload_type : PayloadType
    """


@parse_payload_type.register(str)
def _(payload_type: str) -> PayloadType:
    try:
        return PayloadType[payload_type]
    except KeyError as err:
        raise ValueError(f'Invalid PayloadType {err}') from err


@parse_payload_type.register(int)  # type: ignore
def _(payload_type: int) -> PayloadType:
    return PayloadType(payload_type)
