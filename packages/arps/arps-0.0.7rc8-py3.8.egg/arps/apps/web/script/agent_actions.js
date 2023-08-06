import {request_action} from './rest.js';

const list_agents = async (env_id) => {
    return await request_action(`localhost:5000/${env_id}`, 'list_agents', null, null, 'GET');
};

//expect a json object in the format:
//{ "PolicyName": null, "PolicyName2": 10} //some integer value greater than 1
const spawn_agent = async (env_id, policies) => {
    const payload = {'policies': policies};
    return await request_action(`localhost:5000/${env_id}`, 'agents', null,
                         payload, 'POST');
};

const agent_status = async (env_id, agent_id, request_type) => {
    return await request_action(`localhost:5000/${env_id}`, `agents/${agent_id}`, `request_type=${request_type}`, null, 'GET');
};

const terminate_agent = async (env_id, agent_id) => {
    return await request_action(`localhost:5000/${env_id}`, `agents/${agent_id}`, null, null, 'DELETE');
};

const about = async() => {
    const response = await request_action(`localhost:5000`, 'about', null, null, 'GET');
    return response.json();
};

const list_policies = async(env_id) => {
    const response = await request_action(`localhost:5000/${env_id}`, 'policy_repository', null, null, 'GET');
    return response.json();
};

const update_agent_relationship = async(env_id, agent_from, agent_to, operation) => {
    const payload = {'agent_id': agent_from, 'operation': operation};
    return await request_action(`localhost:5000/${env_id}`, `agents/${agent_to}/relationship`, null, payload, 'PUT');
};

const monitor_logs = async(env_id) => {
    return await request_action(`localhost:5000/${env_id}`, 'monitor_logs', null, null, 'GET');
};

export {about, list_policies, spawn_agent, list_agents, agent_status, terminate_agent, update_agent_relationship, monitor_logs};
