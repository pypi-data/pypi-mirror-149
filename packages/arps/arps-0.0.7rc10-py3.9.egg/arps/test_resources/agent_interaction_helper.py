import asyncio
import contextlib
from typing import Dict, Optional, Type

import pytest_asyncio

from arps.apps.agent_handler import AgentHandler
from arps.core.clock import Clock, simulator_clock_factory
from arps.core.environment import Environment
from arps.core.policy import ReflexPolicy
from arps.core.real.raw_communication_layer import RawCommunicationLayer
from arps.core.real.rest_api_utils import random_port
from arps.core.real.rest_communication_layer import RESTCommunicationLayer
from arps.core.remove_logger_files import remove_logger_files
from arps.test_resources.fake_agents_directory_helper import FakeAgentsDirectoryHelper


@contextlib.contextmanager
def setup_agent_handler(
    policies: Dict[Type[ReflexPolicy], Optional[int]],
    environment: Environment,
    clock: Clock,
    agent_id,
    agents_directory_helper,
    comm_layer_cls,
):
    # Specification of any policies that has touchpoints are required in this tests,
    # since the agent per se does nothing, only provides the interfaces to get info,
    # touchpoint status, and change its policy
    agent_port = random_port()

    policies = policies or {}

    for policy in policies:
        environment.register_policy(policy.__name__, policy)

    policies_by_name = {policy.__name__: period for policy, period in policies.items()}

    try:
        agent_handler = AgentHandler(
            environment=environment,
            clock=clock,
            agent_id=agent_id,
            agent_port=agent_port,
            agents_directory_helper=agents_directory_helper,
            policies=policies_by_name,
            comm_layer_cls=comm_layer_cls,
        )
        yield agent_handler

        remove_logger_files(agent_handler.agent.metrics_logger.logger)
    finally:
        for policy in policies:
            environment.unregister_policy(policy.__name__)


@pytest_asyncio.fixture(params=(RawCommunicationLayer, RESTCommunicationLayer))
async def real_env_components(request):
    agents_directory_helper = FakeAgentsDirectoryHelper()
    clock = simulator_clock_factory()

    clock_task = asyncio.create_task(clock.run())

    yield clock, agents_directory_helper, request.param

    clock_task.cancel()

    await clock_task
