from typing import Dict, List, Optional, Type

from arps.core.mobile_entity import Boundaries
from arps.core.policy import PeriodicPolicy, ReflexPolicy
from arps.core.remove_logger_files import remove_logger_files
from arps.core.touchpoint import Actuator, Sensor


class Environment:
    def __init__(
        self,
        sensors=List[Sensor],
        actuators=List[Actuator],
        boundaries: Optional[Boundaries] = None,
    ):
        """Receives instances that will be used during application
        execution lifetime and need to be accessible by other classes

        Params:
        - sensors : a list of sensors instance
        - actuators : a list of actuators instance
        - boundaries: boundaries with upper and lower coordinates representing the boundaries

        See that sensors and actuator are global while policies will
        be created local required, that why sensor and actuator are
        instances while policies are just a class

        Raises:
        - TypeError if sensors or actuators are not a dict instance

        """

        self._sensors = {sensor.resource_name: sensor for sensor in sensors}
        self._actuators = {actuator.resource_name: actuator for actuator in actuators}
        self.boundaries = boundaries

        if len(self._sensors) != len(sensors):
            raise ValueError('Resources instances cannot be shared among sensors.')
        if len(self._actuators) != len(actuators):
            raise ValueError('Resources instances cannot be shared among actuators.')

        self._registered_policies: Dict[str, Type[ReflexPolicy]] = {}

    @property
    def sensors(self) -> Dict[str, Sensor]:
        return self._sensors

    @property
    def actuators(self) -> Dict[str, Actuator]:
        return self._actuators

    def sensor(self, sensor_category):
        """
        Return sensor global instances based on resource category

        Parameters:
        - sensor_category: resource category

        Raises KeyError when an invalid sensor id is supplied
        """
        return self._sensors[sensor_category]

    def actuator(self, actuator_category):
        """
        Return actuator instances based on resource category

        Parameters:
        - actuator_category: resource category

        Raises KeyError when an invalid actuator id is supplied
        """
        return self._actuators[actuator_category]

    def resources(self):
        """
        Return a dictionary containing touchpoint category as key and touchpoint resource as value
        """
        resources = dict()
        for sensor_category, sensor in self._sensors.items():
            resources[sensor_category] = sensor.resource

        for actuator_category, actuator in self._actuators.items():
            resources[actuator_category] = actuator.resource

        return resources

    def list_registered_policies(self):
        """
        List registered policies

        """
        return list(self._registered_policies.keys())

    def register_policy(self, policy_id: str, policy_class: Type[ReflexPolicy]):
        """
        Register policy class to be available globally

        Args:
        - policy_id : policy unique identification
        - policy_class : policy class
        """
        self._registered_policies[policy_id] = policy_class

    def unregister_policy(self, policy_id: str):
        """
        Removes policy class from the policy repository

        Args:
        - policy_id : policy unique identification
        """

        del self._registered_policies[policy_id]

    def load_policy(self, policy_id: str, period: Optional[int] = None) -> ReflexPolicy:
        """
        Returns a new instance of policy associated with policy id

        Args:
        - policy_id : policy unique identification
        - period: for periodic policies

        Raises:
        - ValueError when no policy in agent_manager is found, or no
        period is provided when using periodic policy
        """
        try:
            policy_instance = self._registered_policies[policy_id]()
        except KeyError:
            raise ValueError(f'Policy {policy_id} not registered')

        valid_period = isinstance(period, int) and period > 0
        if isinstance(policy_instance, PeriodicPolicy) and not valid_period:
            remove_logger_files(policy_instance.logger)
            raise ValueError(
                f'Expected positive int period when creating periodic policy {policy_id}'
            )

        if not isinstance(policy_instance, PeriodicPolicy) and period is not None:
            remove_logger_files(policy_instance.logger)
            raise ValueError(
                f'Trying to use period with a non periodic policy {policy_id}'
            )

        if isinstance(policy_instance, PeriodicPolicy) and period is not None:
            policy_instance.period = period

        return policy_instance

    def is_policy_registered(self, policy_id: str) -> bool:
        """
        Returns True if policy was previously registered, False otherwise

        Args:
        - policy_id : policy identifier
        """
        return policy_id in self._registered_policies

    def __str__(self):
        sensors = list(self.sensors.keys())
        actuators = list(self.actuators.keys())
        if self.boundaries:
            template = 'Environment(sensors={sensors}, actuators={actuators}, boundaries={boundaries})'
            return template.format(
                sensors=sensors, actuators=actuators, boundaries=self.boundaries
            )

        template = 'Environment(sensors={sensors}, actuators={actuators})'
        return template.format(sensors=sensors, actuators=actuators)
