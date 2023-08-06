import platform

import pytest # type: ignore

from arps.core.agent_id_manager import AgentID
from arps.core.payload_factory import PayloadType
from arps.core.real.rest_communication_layer import RESTCommunicationLayer

from arps.core.real.rest_api_utils import (async_invoke_rest_ws,
                                           HTTPMethods,
                                           build_url,
                                           build_http_body_and_header)

from arps.test_resources.fake_agents_directory_helper import FakeAgentsDirectoryHelper
from arps.test_resources.simple_entity import SimpleEntity


@pytest.mark.asyncio
async def test_available_rest_resources():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    url = build_url(endpoint, '/')
    result, status = await async_invoke_rest_ws(HTTPMethods.GET, url)

    assert status.code == 200

    resources_available = result['resources_available']

    assert '/info' in resources_available
    assert '/sensors' in resources_available
    assert '/actuators' in resources_available
    assert '/policy' in resources_available
    assert '/action' in resources_available
    assert '/meta_agent' in resources_available


@pytest.mark.asyncio
async def test_request_invalid_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    url = build_url(endpoint, '/dummy')
    result, status = await async_invoke_rest_ws(HTTPMethods.GET, url)

    assert not result
    assert status.code == 400
    assert status.reason == 'Unsupported request type: dummy. Access / to see list of available resource'

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_info_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    url = build_url(endpoint, '/info')
    result, status = await async_invoke_rest_ws(HTTPMethods.GET, url)

    assert status.code == 200, status.reason
    result['sender_id'] == '0.0'
    result['type'] == 'info'
    result['content']['sensors'] == ['CPU']
    result['content']['actuators'] == ['increase_cpu_frequency',
                                       'decrease_cpu_frequency']
    result['content']['policies'] == ['DummyPolicy()',
                                      'AnotherDummyPolicy()']
    result['content']['related_agents'] == ['0.0', '0.1', '0.2']

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_sensors_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    url = build_url(endpoint, '/sensors')
    result, status = await async_invoke_rest_ws(HTTPMethods.GET, url)

    assert status.code == 200, status.reason
    assert result['sender_id'] == '0.0'
    assert result['type'] == PayloadType.sensors
    assert result['content']['touchpoint'] == {'SensorID': 'sensor_value'}

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_actuators_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    url = build_url(endpoint, '/actuators')
    result, status = await async_invoke_rest_ws(HTTPMethods.GET, url)

    assert status.code == 200, status.reason
    assert result['sender_id'] == '0.0'
    assert result['type'] == PayloadType.actuators
    assert result['content']['touchpoint'] == {'ActuatorID': 'actuator_value'}

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_policy_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    body = {'policy': 'DummyPolicy', 'op': 'add'}
    body, headers = build_http_body_and_header(body)
    url = build_url(endpoint, '/policy')
    result, status = await async_invoke_rest_ws(HTTPMethods.PUT, url, body, headers)

    assert status.code == 200, status.reason
    assert result['sender_id'] == '0.0'
    assert result['type'] == PayloadType.policy
    assert result['content']['status'] == 'Updated successfully'

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_meta_agent_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'
    body = {'agent': '0.1', 'op': 'add'}
    body, headers = build_http_body_and_header(body)
    url = build_url(endpoint, '/meta_agent')
    result, status = await async_invoke_rest_ws(HTTPMethods.PUT, url, body, headers)

    assert status.code == 200, status.reason
    assert result['sender_id'] == '0.0'
    assert result['type'] == PayloadType.meta_agent
    assert result['content']['status'] == 'Updated successfully'

    await entity.communication_layer.close()


@pytest.mark.asyncio
async def test_action_resource():
    agents_directory_helper = FakeAgentsDirectoryHelper()

    agent_id = AgentID(0, 0)

    entity = SimpleEntity(agent_id,
                          agents_directory_helper,
                          RESTCommunicationLayer)

    await entity.communication_layer.start()

    endpoint = f'{platform.node()}:{entity.communication_layer.port}'

    # Albeit not recommended, an action can be empty
    body = {}
    body, headers = build_http_body_and_header(body)
    url = build_url(endpoint, '/action')
    result, status = await async_invoke_rest_ws(HTTPMethods.PUT, url, body, headers)

    assert status.code == 200, status.reason
    assert result['sender_id'] == '0.0'
    assert result['type'] == PayloadType.action
    assert result['content']['status'] == 'Action scheduled to be executed'

    await entity.communication_layer.close()

if __name__ == '__main__':
    pytest.run([__file__])
