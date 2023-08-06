import platform

import pytest # type: ignore

from arps import __version__ as arps_version

from arps.core.real.agents_directory_helper import (AgentsDirectoryHelper,
                                                    AgentsDirectoryHelperError)

from arps.test_resources.apps_runner import start_agents_directory


@pytest.fixture
def agents_directory_helper():
    with start_agents_directory() as agents_directory_port:
        agents_directory = AgentsDirectoryHelper(address=platform.node(),
                                                 port=agents_directory_port)
        yield agents_directory


def test_index(agents_directory_helper):
    result = agents_directory_helper.available_commands()
    create_agent_payload = "Payload: {'id': 'id_value', 'address': 'address', 'port': 'port'}"
    expected = {'available commands': {'/agents/{id}': 'Retrieves agent (GET) or Removes Agent (DELETE)',
                                       '/agents': f'List registered agents (GET) or Creates agent (POST). {create_agent_payload}',
                                       '/about': 'About this service'}}
    assert expected == result


def test_about(agents_directory_helper):
    result = agents_directory_helper.about()
    assert result == f'agent service directory version {arps_version}'


def test_add(agents_directory_helper):
    result = agents_directory_helper.list()
    assert result == dict()

    result = agents_directory_helper.add(agent_id='0.1', address='localhost', port=2001)
    assert result == 'Agent 0.1 added'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}

    result = agents_directory_helper.add(agent_id='0.2', address='localhost', port=2002)
    assert result == 'Agent 0.2 added'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'},
                      '0.2': {'address': 'localhost', 'port': '2002'}}


def test_add_already_added_same(agents_directory_helper):
    result = agents_directory_helper.list()
    assert result == dict()

    result = agents_directory_helper.add(agent_id='0.1', address='localhost', port=2001)
    assert result == 'Agent 0.1 added'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}

    result = agents_directory_helper.add(agent_id='0.1', address='localhost', port=2001)
    assert result == 'Agent 0.1 added'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}


def test_add_already_added_different(agents_directory_helper):
    result = agents_directory_helper.list()
    assert result == dict()

    result = agents_directory_helper.add(agent_id='0.1', address='localhost', port=2001)
    assert result == 'Agent 0.1 added'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}

    with pytest.raises(AgentsDirectoryHelperError) as excinfo:
        agents_directory_helper.add(agent_id='0.1', address='localhost', port=2002)

    assert str(excinfo.value) == 'Agent 0.1 is already added but with different parameters'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}

    with pytest.raises(AgentsDirectoryHelperError) as excinfo:
        agents_directory_helper.add(agent_id='0.1', address='0.0.0.0', port=2001)
    assert str(excinfo.value) == 'Agent 0.1 is already added but with different parameters'

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': 'localhost', 'port': '2001'}}


def test_get(agents_directory_helper):
    agents_directory_helper.add(agent_id='0.1', address=platform.node(), port='2001')
    agents_directory_helper.add(agent_id='0.2', address=platform.node(), port='2002')

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': platform.node(), 'port': '2001'}, '0.2': {'address': platform.node(), 'port': '2002'}}

    result = agents_directory_helper.get(agent_id='0.1')
    assert result == {'address': platform.node(), 'port': '2001'}

    result = agents_directory_helper.get(agent_id='0.2')
    assert result == {'address': platform.node(), 'port': '2002'}


def test_get_fail(agents_directory_helper):
    with pytest.raises(AgentsDirectoryHelperError) as excinfo:
        agents_directory_helper.get(agent_id='0.1')
    assert str(excinfo.value) == 'Agent 0.1 not found'


def test_remove(agents_directory_helper):
    agents_directory_helper.add(agent_id='0.1', address=platform.node(), port=2001)

    result = agents_directory_helper.list()
    assert result == {'0.1': {'address': platform.node(), 'port': '2001'}}

    result = agents_directory_helper.remove(agent_id='0.1')
    assert result == 'Agent 0.1 removed'

    result = agents_directory_helper.list()
    assert {} == result


def test_remove_fail(agents_directory_helper):
    with pytest.raises(AgentsDirectoryHelperError) as excinfo:
        agents_directory_helper.remove(agent_id='0.1')
    assert str(excinfo.value) == 'Agent 0.1 not found'


if __name__ == '__main__':
    pytest.main([__file__])
