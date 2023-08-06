from typing import Tuple
from functools import partial

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import (PayloadType,
                                       Request,
                                       create_policy_response,
                                       create_error_response,
                                       MetaOp)
from arps.core.policy import ActionType, ReflexPolicy


class MetaPolicyProvider(ReflexPolicy):
    '''Provides a way to add, remove other policies

    To add or remove a policy, create a request using
    PayloadFactory.create_policy_request(...)

    If the policy exists, it will perform the operation trhough
    ActionType.event. Otherwise it will return an ActionType.result
    containing:

    - unknown operation, when 'op' content is unknown
    - unknown policy, when PolicyName contains an unregistered policy'

    See tests for more examples.

    '''

    def _condition(self, host, event, epoch) -> bool:
        '''
        Returns True if contains a request of PayloadType.policy
        '''
        if not isinstance(event, Request):
            self.logger.debug('Not a request, condition not met')
            return False

        is_policy = event.type == PayloadType.policy
        self.logger.debug('Event is a policy change request: %s', is_policy)
        return is_policy

    def _action(self, host, event, epoch) -> Tuple[ActionType, bool]:
        '''
        Modifies an agent's policies by adding or removing the specified policy
        '''

        content = event.content

        sender_id = event.sender_id
        receiver_id = event.receiver_id
        message_id = event.message_id

        async def send_error_response(content):
            await host.send(create_error_response(receiver_id,
                                                  sender_id,
                                                  message_id,
                                                  content),
                            AgentID.from_str(sender_id))

        policy_name = content.meta['policy']
        period = content.meta.get('period')

        if not host.is_policy_registered(policy_name):
            content = f'policy {policy_name} not registered'
            self.logger.debug(content)
            action = send_error_response(content)
            return (ActionType.event, action)

        action = None
        operation = content.op

        async def execute(op_function):
            try:
                op_function()

                content = f'operation code {operation} about policy {policy_name} executed successfully'
                await host.send(create_policy_response(receiver_id,
                                                       sender_id,
                                                       content,
                                                       message_id),
                                AgentID.from_str(sender_id))
            except ValueError as err:
                await send_error_response(str(err))

        if operation == MetaOp.add:
            self.logger.info('add policy %s requested', policy_name)
            action = execute(partial(host.add_policy, policy_name, period))
        elif operation == MetaOp.remove:
            self.logger.info(f'remove policy %s requested', policy_name)
            action = execute(partial(host.policies_executor.remove_policy, policy_name))
        else:
            content = f'unknown operation code {operation}'
            self.logger.warning(content)
            action = send_error_response(content)

        return (ActionType.event, action)
