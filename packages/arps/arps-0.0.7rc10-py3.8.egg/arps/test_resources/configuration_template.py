import tempfile
import os
import contextlib
from typing import List, Dict, Optional

import simplejson as json

REAL_ENVIRONMENT_CONF = {
    'run_as_simulator': False,
    'identifier': 0,
    'agents_directory': None,
    'agent_config': None,
    'pmt': None,
    'comm_layer': None
}


@contextlib.contextmanager
def generate_real_env_configuration(agent_conf_path: List[str],
                                    agents_directory: Dict,
                                    comm_layer_type: str,
                                    pmt: Optional[Dict] = None):
    '''
    Generate temporary configuration file to be used in real environment

    Return the path of this file

    Args:
    - agent_conf_path: List containing path to the agent configuration file
    - agents_directory: Dict containing port and address of agents directory service
    - pmt: Dict containing port and address of PMT service; Optional value, can be None
    '''

    assert 'address' in agents_directory and agents_directory['address'] is not None
    assert 'port' in agents_directory and agents_directory['port'] is not None
    assert not pmt or 'address' in pmt and pmt['address'] is not None
    assert not pmt or 'port' in pmt and pmt['port'] is not None
    assert comm_layer_type in ['raw', 'REST']

    real_environment_conf = REAL_ENVIRONMENT_CONF.copy()
    real_environment_conf['agents_directory'] = agents_directory
    real_environment_conf['agent_config'] = agent_conf_path
    if pmt:
        real_environment_conf['pmt'] = pmt
    real_environment_conf['comm_layer'] = comm_layer_type

    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf',
                                     dir=os.getcwd(), delete=False) as tmp:
        json.dump(real_environment_conf, tmp, indent=4)

    try:
        yield tmp.name
    finally:
        os.remove(tmp.name)
