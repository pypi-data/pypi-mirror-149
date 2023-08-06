from typing import Callable, Any
from collections import defaultdict


class EstimatorsTableError(Exception):
    '''
    Error raised when EstimatorsTable isn't used as expected
    '''


class Estimators:
    '''
    Class to group estimators from an environment.

    It contains no method. Methods are added by EstimatorsTable
    '''


class EstimatorsTable:
    '''
    Estimators table stores estimators of each environment
    '''

    def __init__(self):
        self.estimators = defaultdict(Estimators)

    def add_estimator(self, environment: int, estimator_id: str, estimator: Callable[..., Any]) -> None:
        '''
        Add estimator into environment. A method can be accessed using estimator_id.
        Ex.: estimators_table[environment].estimator_id(param)

        Raises EstimatorsTableError if Estimator has already an estimator_id

        Args:
        - environment: environment unique identifier
        - estimator_id: unique estimator_id per environment
        - estimator: function that provides an estimate (ex.: running_time based on problem size)
        '''
        if not hasattr(self.estimators[environment], estimator_id):
            setattr(self.estimators[environment], estimator_id, estimator)
            return

        raise EstimatorsTableError('Estimator already registered for environment {}'.format(environment))

    def __getitem__(self, environment: int):
        '''
        Get estimator from environment

        Raises EstimatorsTableError if environment does not exist

        Args:
        - environment: environment unique identifier
        '''
        if environment not in self.estimators:
            raise EstimatorsTableError('Invalid environment {}'.format(environment))

        return self.estimators[environment]
