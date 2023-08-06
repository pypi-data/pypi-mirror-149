import copy
import importlib
import logging
import pathlib
from collections import namedtuple
from typing import Any, Dict, List, Optional, Tuple

import simplejson as json

from arps.core.environment import Environment
from arps.core.mobile_entity import Boundaries, Coordinates
from arps.core.policies.monitor import MonitorType, build_monitor_policy_class
from arps.core.resources_table import Resources, ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.event_queue_loader import (
    EventQueueLoader,
    FileEventQueueLoader,
    RandomEventQueueLoader,
)
from arps.core.touchpoint import TouchPoint

CoordinatesType = Tuple[int, int, int]


class InvalidConfigurationError(Exception):
    """General exception to be used when something unexpected is
    encountered by the parser

    """


logger = logging.getLogger('ConfigurationFileLoader')

SimulatorManagerEnvironment = namedtuple(
    'SimulatorManagerEnvironment',
    [
        'run_as_simulator',
        'resources_table',
        'configuration',
        'event_queue_loader',
        'sim_event_scheduler',
        'results_path',
        'log_formatter',
        'pmt',
    ],
)


def load_manager_environment(conf_file_path):
    with open(conf_file_path) as conf_path:
        parsed_configuration = json.loads(conf_path.read())

        run_as_simulator = parsed_configuration['run_as_simulator']
        if not run_as_simulator:
            RealManagerEnvironment = namedtuple('RealManagerEnvironment', ['run_as_simulator', 'configuration'])
            return RealManagerEnvironment(run_as_simulator, _load_real_environment(parsed_configuration))

        user_defined_base_module = parsed_configuration['user_defined_base_module']

        environments = parsed_configuration['environments']
        environment_types = dict()

        def is_multiple_ids(manager_id):
            return isinstance(manager_id, str) and '..' in manager_id

        # separate environments declared as homonegeous from the individual environments
        environments_single_id = [manager for manager in environments if not is_multiple_ids(manager['identifier'])]
        environments_multiple_ids = [manager for manager in environments if is_multiple_ids(manager['identifier'])]

        # load all environments declared as START..END into the individual environments
        for manager in environments_multiple_ids:
            start_id, end_id = manager['identifier'].split('..')
            start_id, end_id = int(start_id), int(end_id)
            if end_id < start_id or start_id < 0:
                message = 'Error while creating homogeneous environment. Reason: {reason}'
                raise InvalidConfigurationError(
                    message.format(
                        reason='start id must be greater or equal than 0 and start id must be less than end id'
                    )
                )

            for identifier in range(start_id, end_id + 1):
                new_manager = copy.deepcopy(manager)
                new_manager['identifier'] = identifier
                environments_single_id.append(new_manager)

        environments = environments_single_id
        environment_types = {manager['identifier']: manager['type'] for manager in environments}
        resources_table = ResourcesTable(environment_types)

        for manager in environments:
            load_resources_table(
                manager['identifier'],
                resources_table,
                user_defined_base_module,
                manager['resources'],
            )

        loaded_managers = [
            _load_sim_environment(resources_table, user_defined_base_module, manager) for manager in environments
        ]

        for manager in environments:
            _create_relationship_between_manager_resources(manager, resources_table)

        simulator_configuration = parsed_configuration['simulator']
        event_queue_loader = load_event_queue_loader(simulator_configuration['event_queue'], resources_table)

        simulation_results_path = pathlib.Path(*simulator_configuration['results_path'])
        simulation_log_formatter = simulator_configuration['log_formatter']

        scheduler = simulator_configuration['scheduler']
        scheduler_class = load_attribute(module_path=scheduler['module'], attribute_name=scheduler['class'])
        sim_event_scheduler = scheduler_class(resources_table.environments)

        return SimulatorManagerEnvironment(
            run_as_simulator,
            resources_table,
            loaded_managers,
            event_queue_loader,
            sim_event_scheduler,
            simulation_results_path,
            simulation_log_formatter,
            parsed_configuration.get('pmt'),
        )


def _create_relationship_between_manager_resources(manager, resources_table: ResourcesTable):
    """
    Used for simulation only.

    Create a relationship between affected resource and resource that
    indirect affects.

    A resource can affect and be affected by many other resources.

    Args:
    - manager: Manager with information needed to create the
      relationship between resources
    - resources_table: Resources table containing resources from each
      environment and organized by their identifier
    """
    for affecting_resource in manager['resources']:
        affected_identifier = affecting_resource.get('affects', None)
        if not affected_identifier:
            continue

        for affected_manager_id, affected_resources_id in affected_identifier.items():
            for affected_resource_id in affected_resources_id:
                resources = resources_table.resources_from_environment(environment_id=manager['identifier'])
                resource_instance_affecting = resources[affecting_resource['class']]

                resources = resources_table.resources_from_environment(environment_id=int(affected_manager_id))
                resource_instance_affected = resources[affected_resource_id]

                resource_instance_affecting.affects(resource_instance_affected)


def _load_real_environment(configuration):
    ManagerConfiguration = namedtuple(
        'ManagerConfiguration',
        ['identifier', 'agent_config', 'agents_directory', 'pmt', 'comm_layer_type'],
    )

    return ManagerConfiguration(
        configuration['identifier'],
        pathlib.Path(*configuration['agent_config']),
        configuration['agents_directory'],
        configuration.get('pmt'),
        configuration['comm_layer'],
    )


def _load_sim_environment(resources_table: ResourcesTable, user_defined_base_module: str, environment: Dict):
    ManagerConfiguration = namedtuple('ManagerConfiguration', ['identifier', 'agent_environment'])

    identifier = environment['identifier']
    boundaries = _load_boundaries(environment.get('boundaries'))

    agent_environment = _load_agent_environment(
        identifier,
        user_defined_base_module,
        environment,
        resources_table.resources_from_environment(environment_id=identifier),
        boundaries,
    )

    return ManagerConfiguration(identifier, agent_environment)


def _load_boundaries(boundaries: Optional[Dict[str, CoordinatesType]]) -> Optional[Boundaries]:
    if boundaries is None:
        return None

    lower_bound = boundaries.get('lower_bound')
    upper_bound = boundaries.get('upper_bound')

    assert lower_bound is not None and upper_bound is not None

    return Boundaries(Coordinates(*upper_bound), Coordinates(*lower_bound))


def load_agent_environment(identifier: int, agent_conf_file: pathlib.Path):
    """
    Args:
    - identifier: identifier of the environment which the agent is part
    - agent_conf_file: path to the agent configuration file
    """

    try:
        with open(agent_conf_file, 'r') as agent_conf:
            agent_properties = json.loads(agent_conf.read())

            user_defined_base_module = agent_properties['user_defined_base_module']

            resources_table = ResourcesTable(environment_types={identifier: identifier})
            load_resources_table(
                identifier,
                resources_table,
                user_defined_base_module,
                agent_properties['resources'],
            )

            boundaries = _load_boundaries(agent_properties.get('boundaries'))

            return _load_agent_environment(
                identifier,
                user_defined_base_module,
                agent_properties,
                resources_table.resources_from_environment(environment_id=identifier),
                boundaries,
            )
    except FileNotFoundError:
        raise InvalidConfigurationError(f'agent config file {agent_conf_file} doesn\'t exist')


def _load_agent_environment(
    identifier: int,
    user_defined_base_module: str,
    agent_properties: Dict[str, Any],
    resources_in_environment: Resources,
    boundaries: Optional[Boundaries],
):
    """
    Load agent environment.
    Create instances of resource classes and link to its sensors and actuators.
    Register policies to be associated with agents

    Args:
    - identifier : agent manager identifier
    - user_defined_base_module : base module where resources,
      touchpoints and policies can be found
    - agent_properties : dict containing sensors, actuators, and policies
    - resources_in_environment : resources organized by their categories
    - boundaries: boundaries instance containing upper and lower bound coordinates respectively
    """

    agent_configuration = agent_properties['agent_config']
    sensors = _load_touchpoint_instances(
        resources_in_environment,
        user_defined_base_module,
        agent_configuration['sensors'],
    )
    actuators = _load_touchpoint_instances(
        resources_in_environment,
        user_defined_base_module,
        agent_configuration['actuators'],
    )

    environment = Environment(sensors=sensors, actuators=actuators, boundaries=boundaries)

    policies = agent_configuration['policies']
    for policy in policies:
        policy_cls = load_attribute(
            module_base_path=user_defined_base_module,
            module_path='policies',
            attribute_name=policy,
        )
        environment.register_policy(policy_cls.__name__, policy_cls)

    for sensor in sensors:
        monitor_sensor_policy_cls = build_monitor_policy_class(
            f'{sensor.resource_name}MonitorPolicy',
            touchpoint_category=sensor.resource_name,
            monitor_type=MonitorType.Sensor,
        )
        environment.register_policy(monitor_sensor_policy_cls.__name__, monitor_sensor_policy_cls)

    for actuator in actuators:
        monitor_actuator_policy_cls = build_monitor_policy_class(
            f'{actuator.resource_name}MonitorPolicy',
            touchpoint_category=actuator.resource_name,
            monitor_type=MonitorType.Actuator,
        )
        environment.register_policy(monitor_actuator_policy_cls.__name__, monitor_actuator_policy_cls)

    logger.info('loaded resources %s for environment %s', resources_in_environment, identifier)
    logger.info('loaded sensors %s for environment %s', sensors, identifier)
    logger.info('loaded actuators %s for environment %s', actuators, identifier)
    logger.info('loaded policies %s for environment %s', policies, identifier)

    return environment


def load_resources_table(
    environment_identifier: int,
    resources_table: ResourcesTable,
    resources_module: str,
    resources,
) -> None:
    """
    Load resources in their categories.

    Args:
    - environment_identifier: environment identifier
    - resources_table : resources classified by their categories in
      each environment
    - resources_module : where the resources module is
    - resources : dict file containing resources descriptions. Each
      resource is composed of:
        - id: unique global identifier of the instance that will be
          created
        - initial_state: initial value of the resource
        - attribute: customizable attribute that can be accessed by the class
        - affects: unique global identifier of resource that will be
          affected by this resource
            * This parameter is used during simulations only
    """

    for resource in resources:
        initial_state = resource.get('initial_state')
        attributes = resource.get('attributes')
        resource_cls = load_attribute(
            module_base_path=resources_module,
            module_path='resources',
            attribute_name=resource['class'],
        )
        if resource_cls in resources_table.resources_from_environment(environment_id=environment_identifier):
            continue

        if initial_state and attributes:
            resource_instance = resource_cls(
                environment_identifier=environment_identifier,
                initial_state=initial_state,
                attributes=attributes,
            )
        elif attributes:
            resource_instance = resource_cls(environment_identifier=environment_identifier, attributes=attributes)
        elif initial_state:
            resource_instance = resource_cls(
                environment_identifier=environment_identifier,
                initial_state=initial_state,
            )
        else:
            resource_instance = resource_cls(environment_identifier=environment_identifier)
        resources_table.add_resource(resource_instance)


def load_event_queue_loader(event_queue_properties: Dict, resources_table: ResourcesTable) -> EventQueueLoader:
    """
    Create loader that will return next simulation event

    Args:

    - event_queue_properties: dict containing module, classes and so on to import correct loader
    and to open the tracefile or the random event generator
    - resources_table: Resources table containing resources from each
      environment and organized by their categories
    """
    generator = event_queue_properties['generator']
    event_factory = generator['factory']
    event_factory_cls = load_attribute(module_path=event_factory['module'], attribute_name=event_factory['class'])

    estimators_table = build_estimators_table(event_queue_properties)

    event_factory_instance = event_factory_cls(resources_table, estimators_table)

    if not event_queue_properties['deterministic']:
        random_generator = generator['random']
        random_generator_cls = load_attribute(
            module_path=random_generator['module'],
            attribute_name=random_generator['class'],
        )
        number_of_random_events = generator.get('number_of_random_events')
        return RandomEventQueueLoader(event_factory_instance, random_generator_cls(), number_of_random_events)

    event_queue_file = pathlib.Path(*generator['file'])
    return FileEventQueueLoader(event_queue_file, event_factory_instance)


def build_estimators_table(event_queue_properties):
    estimators_table = EstimatorsTable()
    if 'resources_estimator' not in event_queue_properties:
        return estimators_table

    for estimators in event_queue_properties['resources_estimator']:
        environment = estimators['environment']
        for estimator in estimators['estimators']:
            estimator_name = estimator['name']
            module = estimator['module']
            estimator_func_name = estimator['estimator']
            estimator_func = load_attribute(module_path=module, attribute_name=estimator_func_name)
            estimators_table.add_estimator(environment, estimator_name, estimator_func)
    return estimators_table


def _load_touchpoint_instances(
    resources: Resources, touchpoints_base_module: str, touchpoints_properties
) -> List[TouchPoint]:
    touchpoints = list()

    for touchpoint_properties in touchpoints_properties:
        touchpoint_class_name = touchpoint_properties['class']
        resource_id = touchpoint_properties['resource_id']
        touchpoint_class = load_attribute(
            module_base_path=touchpoints_base_module,
            module_path='touchpoints',
            attribute_name=touchpoint_class_name,
        )
        touchpoint_instance = touchpoint_class(resources[resource_id])
        touchpoints.append(touchpoint_instance)

    return touchpoints


def load_attribute(*, module_base_path: str = '', module_path: str, attribute_name: str):
    """
    Load attribute from configuration file

    Args:
    - module_path: python syntax module, i.e., "package1.package2.module"
    - attribute_name: attribute to be loaded (class or function)
    """
    relative_module_base_path = module_base_path.startswith('.') and len(module_base_path) >= 2
    relative_module_path = module_path.startswith('.') and len(module_path) >= 2
    if relative_module_base_path or relative_module_path:
        raise InvalidConfigurationError('Relative import is not allowed')

    if module_base_path == '.':
        module_base_path = ''

    if module_base_path:
        module_path = module_base_path + '.' + module_path

    try:
        logger.info('Loading attribute %s from module %s', attribute_name, module_path)
        module = importlib.import_module(module_path)
        attribute = getattr(module, attribute_name)
    except ImportError as import_error:
        raise InvalidConfigurationError(str(import_error) + ', check if module or attribute name exists')
    except ValueError as value_error:
        raise InvalidConfigurationError(str(value_error) + ', check module')
    except AttributeError as attribute_error:
        raise InvalidConfigurationError(str(attribute_error) + ', check attribute name')

    return attribute
