from functools import partial
from typing import Any, Tuple

from arps.core.mobile_entity import Axis
from arps.core.policy import ActionType, PeriodicPolicy


class MoveWithinBoundariesPolicy(PeriodicPolicy):
    def _action(self, host, event, epoch) -> Tuple[ActionType, Any]:
        action = partial(host.move, 1, axis=Axis.X)
        return (ActionType.event, action)


class CaptureAndMoveResourcePolicy(PeriodicPolicy):
    def _action(self, host, event, epoch) -> Tuple[ActionType, Any]:
        mobile_resources_state = host.read_sensor("MobileResources")

        owned_resources = {
            key: mobile_resource_state
            for key, mobile_resource_state in mobile_resources_state.items()
            if mobile_resource_state["owner"] == host.identifier and mobile_resource_state["active"]
        }
        available_resources = {
            key: mobile_resource_state
            for key, mobile_resource_state in mobile_resources_state.items()
            if mobile_resource_state["owner"] is None and mobile_resource_state["active"]
        }

        if not owned_resources and not available_resources:
            return (ActionType.result, f"No resource available for {host.identifier}")

        try:
            resource_key, resource = next((key, value) for key, value in owned_resources.items())
        except StopIteration:
            # No resource associated with this host
            try:
                resource_key, resource = next((key, value) for key, value in available_resources.items())
            except StopIteration:
                return (ActionType.result, "Resource already in its proper place")

        def move_host_to_target(target_coordinates):
            if target_coordinates.x != host.coordinates.x:
                if (target_coordinates.x - host.coordinates.x) > 0:
                    host.move(1, axis=Axis.X)
                else:
                    host.move(-1, axis=Axis.X)
            elif target_coordinates.y != host.coordinates.y:
                if (target_coordinates.y - host.coordinates.y) > 0:
                    host.move(1, axis=Axis.Y)
                else:
                    host.move(-1, axis=Axis.Y)
            elif target_coordinates.z != host.coordinates.z:
                if (target_coordinates.z - host.coordinates.z) > 0:
                    host.move(1, axis=Axis.Z)
                else:
                    host.move(-1, axis=Axis.Z)

        def capture_and_move_along():
            if resource["owner"] is None:
                # Go after the resource
                move_host_to_target(resource["coordinates"])
                if host.coordinates == resource["coordinates"]:
                    resource["owner"] = host.identifier
                    host.modify_actuator(
                        "MobileResources", value={resource_key: resource}, epoch=epoch, identifier=host.identifier
                    )
            elif resource["owner"] == host.identifier:
                # Move when the resource is acquired
                move_host_to_target(resource["target_coordinates"])
                resource["coordinates"] = host.coordinates
                if host.coordinates == resource["target_coordinates"]:
                    resource["active"] = False
                host.modify_actuator(
                    "MobileResources", value={resource_key: resource}, epoch=epoch, identifier=host.identifier
                )

        return (ActionType.event, capture_and_move_along)
