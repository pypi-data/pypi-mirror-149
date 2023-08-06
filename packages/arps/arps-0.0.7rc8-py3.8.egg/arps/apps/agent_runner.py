import argparse
import sys
import logging
import signal
import platform
import asyncio

from arps import __version__ as arps_version
import arps.core
arps.core.initialize_real_environment()

from arps.core.agent_id_manager import AgentID
from arps.core.real.raw_communication_layer import RawCommunicationLayer
from arps.core.real.rest_communication_layer import RESTCommunicationLayer
from arps.core.real.agents_directory_helper import AgentsDirectoryHelper
from arps.core.clock import real_time_clock_factory
from arps.core import logger_setup
from arps.core.remove_logger_files import remove_logger_files
from arps.apps.configuration_file_loader import (load_agent_environment,
                                                 InvalidConfigurationError)
from arps.apps.pid import create_pid_file
from arps.apps.agent_handler import AgentHandler

# pylint: disable-msg=C0103


def main():
    # with open('agent_runner.log', 'a') as f:
    #     f.write(str(os.getpid()) + '\n')

    parser = build_argument_parser()

    try:
        parsed_args = parser.parse_args()
    except argparse.ArgumentTypeError as err:
        sys.exit(err)

    if platform.system() == 'Windows':
        def interrupt_application(*_):
            print('Received signal to stop')
            raise KeyboardInterrupt
        signal.signal(signal.SIGBREAK, interrupt_application)

    try:
        asyncio.run(run_agent(parsed_args))
    except KeyboardInterrupt:
        print('agent finished')


async def run_agent(parsed_args):
    agent_id = AgentID(parsed_args.id[0], parsed_args.id[1])
    logger = logging.getLogger()
    if not parsed_args.quiet:
        logger_setup.set_to_rotate(logger,
                                   level=logging.INFO,
                                   file_name_prefix=f'agent_{agent_id}')
    try:
        environment = load_agent_environment(parsed_args.id[0], parsed_args.config_file)
    except InvalidConfigurationError as error:
        remove_logger_files(logger)
        sys.exit(error)
    agents_directory_helper = AgentsDirectoryHelper(address=parsed_args.agents_dir_addr,
                                                    port=parsed_args.agents_dir_port)

    if not environment:
        remove_logger_files(logger)
        raise 'Required configuration files not present. Check again'

    clock = real_time_clock_factory()

    if parsed_args.comm_layer == 'raw':
        comm_layer_cls = RawCommunicationLayer
    elif parsed_args.comm_layer == 'REST':
        comm_layer_cls = RESTCommunicationLayer
    else:
        remove_logger_files(logger)
        raise ValueError('Invalid Communication Layer selected. Expect raw or REST')

    try:
        policies = {**parsed_args.policy, **parsed_args.periodic_policy}
        agent_handler = AgentHandler(environment=environment,
                                     clock=clock,
                                     agent_id=agent_id,
                                     agent_port=parsed_args.port,
                                     policies=policies,
                                     agents_directory_helper=agents_directory_helper,
                                     comm_layer_cls=comm_layer_cls)
    except RuntimeError as e:
        remove_logger_files(logger)
        sys.exit(e)

    await agent_handler.start()

    with create_pid_file():
        await clock.run()

    await agent_handler.finalize()


def build_argument_parser():
    parser = argparse.ArgumentParser(description='Instantiates an agent with default policies Info and TouchPointStatus')
    parser.add_argument('--id', nargs=2, type=int, required=True, metavar=('Manager id', 'agent id'),
                        help='identifier of the agent creator')
    parser.add_argument('--port', type=int, default=8888,
                        help='agent listen port (default: %(default)s)')
    parser.add_argument('--policy', action=policy_parser(), nargs=1, metavar=('policy'), default={},
                        help='regular policy that handle events. Can be invoked multiple times for each policy')
    parser.add_argument('--periodic_policy', action=policy_parser(), nargs=2, metavar=('policy', 'period'), default={},
                        help='periodic policy that handle events. Can be invoked multiple times for each policy')
    parser.add_argument('--agents_dir_addr', default='localhost',
                        help='agent directory server address')
    parser.add_argument('--agents_dir_port', default=1500, help='agent directory server port')
    parser.add_argument('--config_file', required=True,
                        help='configuration containing domain specific classes (sensors, actuators, and policies)')
    parser.add_argument('--comm_layer', required=True,
                        choices=['REST', 'raw'],
                        help='Type of communication layer used. Options: REST or raw')
    parser.add_argument('--quiet', default=False,
                        action='store_const', const=True, help='No log generated')
    parser.add_argument('--version', action='version', version=f'ARPS {arps_version}')
    return parser


def format(values):
    if len(values) == 2:
        try:
            return values[0], int(values[1])
        except ValueError:
            return values[0], values[1]
    elif len(values) == 1:
        return values[0], None
    else:
        raise argparse.ArgumentTypeError('Unexpected number of arguments.')


def policy_parser():
    class PolicyAction(argparse.Action):
        """Action to assign a string and optional integer"""
        def __call__(self, parser, namespace, values, option_string=None):
            values = format(values)
            if getattr(namespace, self.dest) is None:
                setattr(namespace, self.dest, dict(values))
                return

            if values[0] in getattr(namespace, self.dest):
                raise argparse.ArgumentTypeError('Only one instance of a policy is allowed. Check if a policy is being added more than once')
            getattr(namespace, self.dest)[values[0]] = values[1]

    return PolicyAction


if __name__ == '__main__':
    main()
    sys.exit(0)
