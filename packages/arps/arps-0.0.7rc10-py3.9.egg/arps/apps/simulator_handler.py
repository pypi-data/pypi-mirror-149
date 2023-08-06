import asyncio
import io
import json
import logging
import os
import pathlib
import time
from contextlib import ExitStack, asynccontextmanager
from functools import partial
from typing import List, NamedTuple, TextIO, Tuple
from zipfile import ZipFile

from arps.core.clock import Clock
from arps.core.simulator.simulator import Simulator

from .configuration_file_loader import SimulatorManagerEnvironment


class SimulatorHandler:
    """
    Class to encapsute operations of the simulator
    """

    class Profile(NamedTuple):
        tracemalloc: List[str]
        total_memory: str

    def __init__(self, clock: Clock, simulator_environment: SimulatorManagerEnvironment) -> None:
        self.clock = clock
        self.sim_env = simulator_environment
        self.sim_log_name = None
        self.sim_event_logger_name = None
        self._running_task = None
        self.clock_run_task = None
        self.elapsed_time = 0
        self.debug = False
        self.profile = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_debug(self, debug: bool):
        self.debug = debug

    @property
    def running(self) -> bool:
        return self._running_task is not None and not self._running_task.done()

    async def log_finished_events(self, simulator: Simulator, sim_event_log_file: TextIO):
        header = 'identifier;environment;arrival_time;start_time;finished_time;info\n'
        sim_event_log_file.write(header)
        while True:
            try:
                event = await asyncio.wait_for(simulator._finished_events.get(), timeout=1)
            except asyncio.CancelledError:
                break
            except asyncio.TimeoutError:
                continue
            except RuntimeError as err:
                self.logger.error('Error while logging events: %s', err)
                raise
            else:
                event_row = f'{event.identifier};{event.environment_id};{event.arrival_time};'
                event_row += f'{event.start_time};{event.finished_time};{event.info}\n'
                sim_event_log_file.write(event_row)
        assert simulator._finished_events.empty()

    def run(self):
        """
        starts clock and simulator

        Return message about the status
        """
        self.logger.info('starting sim handler')

        if not self.running:
            self.logger.info('simulator not running, starting ...')
            self._running_task = asyncio.create_task(self.async_run())
            self.clock_run_task = asyncio.ensure_future(self.clock.run())

    async def async_run(self):
        """Setup sim to run asynchronously"""
        start = time.time()

        if self.debug:
            import tracemalloc

            tracemalloc.start()

        self.logger.info('setting up simulation')

        async with self.setup() as simulator:
            try:
                self.logger.info('simulation started')
                while not simulator.finished:
                    await self.clock.wait_for_notified_tasks()

                self.logger.info('sim has finished')

                # wait 10 steps to cancel the clock
                future = self.clock.epoch_time.epoch + 10
                while self.clock.epoch_time.epoch < future:
                    await asyncio.sleep(0)
            except asyncio.CancelledError:
                self.logger.info('simulation stop requested')
            finally:
                self.clock_run_task.cancel()
                await self.clock_run_task

        self.elapsed_time = time.time() - start

        if self.debug:
            snapshot = tracemalloc.take_snapshot()
            snapshot = snapshot.filter_traces(
                (
                    tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
                    tracemalloc.Filter(False, "<unknown>"),
                    tracemalloc.Filter(False, "*versions/*/lib/python*"),
                    tracemalloc.Filter(False, "*/lib/python*/site-packages/*"),
                )
            )
            snapshot_stats = snapshot.statistics('lineno')
            total = sum(stat.size for stat in snapshot_stats) / 1024
            unit = 'KiB'
            if total > 1024:
                total /= 1024
                unit = 'MiB'

            self.profile = SimulatorHandler.Profile([str(i) for i in snapshot_stats[:10]], f'{total:.2f} {unit}')

            tracemalloc.stop()

    @asynccontextmanager
    async def setup(self):
        """
        Prepare the environment for running a new simulation
        """
        simulator_results_path = self.sim_env.results_path
        if not os.path.exists(simulator_results_path):
            self.logger.info('saving sim result to %s', simulator_results_path)
            os.makedirs(simulator_results_path)

        current_time = time.strftime('%Y%m%d-%H%M%S')
        LOG_TEMPLATE = '{time}_{pid}_{ftype}.log'
        self.sim_log_name = os.path.join(
            simulator_results_path, LOG_TEMPLATE.format(time=current_time, pid=os.getpid(), ftype='sim_results')
        )
        self.sim_event_logger_name = os.path.join(
            simulator_results_path, LOG_TEMPLATE.format(time=current_time, pid=os.getpid(), ftype='events')
        )

        def log_resources_modification(log_file, event):
            entry = (
                f'{event.env};{event.identifier};{event.epoch};{event.value};{str(event.modifier_id)};{event.type}\n'
            )
            log_file.write(entry)

        self.logger.info('sim result log filename is %s', self.sim_log_name)
        with ExitStack() as exit_stack:
            sim_log_file = exit_stack.enter_context(open(self.sim_log_name, 'a'))
            sim_log_file.write('env;identifier;epoch;value;modifier;type\n')

            track_resources_modification = partial(log_resources_modification, sim_log_file)
            simulator = Simulator(self.sim_env.event_queue_loader, self.sim_env.sim_event_scheduler)
            self.clock.add_listener(simulator.step)
            self.sim_env.resources_table.reset()

            sim_event_file = exit_stack.enter_context(open(self.sim_event_logger_name, 'a'))
            sim_event_logger = asyncio.create_task(self.log_finished_events(simulator, sim_event_file))

            self.logger.info('adding resources tracking')
            self.sim_env.resources_table.add_resources_listener(track_resources_modification)

            yield simulator

            sim_event_logger.cancel()

            await sim_event_logger

            self.logger.info('close file name %s', sim_log_file.name)

            self.logger.info('removing resources tracking')
            self.sim_env.resources_table.remove_resources_listener(track_resources_modification)

    def status(self):
        """Retrieve the current state of the simulation, i. e., running or
        stopped

        """
        state = 'running' if self.running else 'stopped'
        self.logger.info('simulation status requested: %s', state)

        return state

    async def stop(self):
        """Stop simulation"""
        if self.running:
            self.logger.info('stopping simulation')
            self.logger.info('%s', self._running_task)
            self._running_task.cancel()
            start = time.time()
            await self._running_task
            self.logger.info('simulation has stopped %s', time.time() - start)

    def simulation_results(self) -> Tuple[pathlib.Path, pathlib.Path]:
        """Return the path to the result of the simulation.

        If the simulation is still running, or the log is nowhere to
        be found, raise RuntimeError

        """
        if self.running:
            raise RuntimeError('Simulation is still running; request stop before requesting result')

        if not (self.sim_log_name and os.path.exists(self.sim_log_name)):
            raise RuntimeError('Simulation log not found')

        if not (self.sim_event_logger_name and os.path.exists(self.sim_event_logger_name)):
            raise RuntimeError('Simulation event log not found')

        return pathlib.Path(self.sim_log_name), pathlib.Path(self.sim_event_logger_name)

    def metadata(self):
        """Returns a dictionary containing the resource as key and how to
        interpret it as value

        """
        metadata = dict()
        for resource in self.sim_env.resources_table.resources():
            resource_name = resource.__class__.__name__
            valid_range = resource.category.valid_range
            value_type = resource.category.value_type.name
            metadata[resource_name] = {'range': valid_range, 'type': value_type}
        return metadata

    def result(self) -> Tuple[bytes, str]:
        sim_results_path, sim_event_path = self.simulation_results()
        zip_file = io.BytesIO()
        with ZipFile(zip_file, 'w') as result_bundle:
            result_bundle.write(sim_results_path)
            result_bundle.write(sim_event_path)
            result_bundle.writestr(str(sim_results_path.with_suffix('.json')), json.dumps(self.metadata()))
        zip_file.seek(0)
        return zip_file.getvalue(), sim_results_path.with_suffix('.zip').name

    def save(self, agent_managers):
        """
        Save actions performed by agent managers and return it for
        future execution

        """
        result = {}
        for agent_manager_id, tracked_actions in agent_managers.items():
            commands = list()
            for action, params in tracked_actions:
                command = {'command': action, 'params': {k: v for (k, v) in params}}
                commands.append(command)
            result[agent_manager_id] = commands
        return result

    def stats(self):
        """Stats from the last simulation"""
        elapsed_time = f'{self.elapsed_time:.2f} seconds'
        if not self.debug:
            return {'elapsed_time': elapsed_time}

        if not self.profile:
            raise RuntimeError('No simulation has been executed so far')

        return {
            'elapsed_time': elapsed_time,
            'total_memory': self.profile.total_memory,
            'tracemalloc': self.profile.tracemalloc,
        }
