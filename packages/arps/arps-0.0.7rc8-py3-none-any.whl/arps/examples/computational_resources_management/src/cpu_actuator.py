from arps.core.touchpoint import Actuator

class CPUActuator(Actuator):

    def _set(self, tracked_value):
        '''
        Controls cpu frequency

        Args:
        - TrackedValue
            - value: pair with target frequency and governor
            - identifier: who is modifying this resource
            - epoch: when it is being modified
            - evt_type: what kind of event triggered the modification

        '''
        value, epoch, identifier, evt_type = tracked_value
        self.resource.modify_value(value,
                                   epoch,
                                   identifier,
                                   evt_type)
