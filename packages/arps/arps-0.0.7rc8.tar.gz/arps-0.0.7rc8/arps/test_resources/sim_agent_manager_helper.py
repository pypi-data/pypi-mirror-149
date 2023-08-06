import contextlib

from arps.core.clock import simulator_clock_factory
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer

from arps.apps.configuration_file_loader import load_manager_environment
from arps.apps.simulator_environment_agent_manager import SimulatorEnvironmentAgentManager


@contextlib.contextmanager
def setup_sim_agent_manager_environment(configuration_path):
    manager_environment = load_manager_environment(configuration_path)
    assert manager_environment.run_as_simulator
    for identifier, env in enumerate(manager_environment.configuration):
        assert env.identifier == identifier

    clock = simulator_clock_factory()

    yield clock, manager_environment


async def build_sim_agent_manager(sim_environment):
    clock, manager_environment = sim_environment

    comm_layer = FakeCommunicationLayer()

    sim_agent_managers = list()
    for manager_configuration in manager_environment.configuration:
        agent_manager = SimulatorEnvironmentAgentManager(manager_configuration=manager_configuration,
                                                         communication_layer=comm_layer,
                                                         clock=clock)
        await agent_manager.start()
        sim_agent_managers.append(agent_manager)

    return sim_agent_managers
