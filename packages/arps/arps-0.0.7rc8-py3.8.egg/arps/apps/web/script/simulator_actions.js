import {request_action} from './rest.js';

const sim_action = async (action) => {
    return await request_action('localhost:5000/sim', `${action}`, null, null, 'GET');
};

const sim_run = async () => {
    return await sim_action('run');
};

const sim_status = async () => {
    return await sim_action('status');
};

const sim_stop = async () => {
    return await sim_action('stop');
};

const sim_result = async () => {
    return await sim_action('result');
};

const sim_save = async () => {
    return await sim_action('save');
};

const sim_stats = async () => {
    return await sim_action('stats');
};

export {sim_run, sim_status, sim_stop, sim_result, sim_save, sim_stats};
