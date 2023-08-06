import '@babel/polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import {createStore} from 'redux';
import {composeWithDevTools} from 'redux-devtools-extension';

import {about, list_policies, spawn_agent, list_agents, agent_status,
        terminate_agent, update_agent_relationship, monitor_logs} from './agent_actions.js';
import {sim_run, sim_status, sim_stop, sim_result, sim_save, sim_stats} from './simulator_actions.js';

//Environment State
const create_environment = ({envs}) => ({
    type: 'CREATE_ENV',
    envs
});

const add_agent = ({env_id, agent}) => ({
    type: 'ADD_AGENT',
    env_id: env_id,
    agent: agent
});

const remove_agents = ({env_id, agents}) => ({
    type: 'REMOVE_AGENTS',
    env_id: env_id,
    agents: agents
});

const environmentReducer = (state = { envs: {} }, action) => {
    switch(action.type) {
    case 'CREATE_ENV':
        state.envs = action.envs;
        return {envs: state.envs};
    case 'ADD_AGENT':
        state.envs[action.env_id].add(action.agent);
        return {envs: state.envs};
    case 'REMOVE_AGENTS':
        for(let agent of action.agents)
            state.envs[action.env_id].delete(agent);
        return {envs: state.envs};
    default:
        return state;
    }
};

const store = createStore(environmentReducer,
                          composeWithDevTools());

// Simulation State
const run_simulation = () => ({
    type: 'RUN_SIM'
});

const stop_simulation = () => ({
    type: 'STOP_SIM'
});

const simulationReducer = (state = {running: false}, action) => {
    switch(action.type) {
    case 'RUN_SIM':
        state = {running: true};
        return state;
    case 'STOP_SIM':
        state = {running: false};
        return state;
    default:
        return state;
    }
};

const sim_store = createStore(simulationReducer,
                              composeWithDevTools());

// Components

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { env_type: null,
                       environments: null,
                       version: null};
    }

    async componentDidMount() {
        const data = await about();
        const env_type = data['simulation'] ? 'Simulated' : 'Real';
        const environments = data['agent_managers'];

        this.setState({ env_type: env_type, version: data['version'],
                        environments: environments});

        let envs = {};
        for(let env_id of environments)
        {
            const response = await list_agents(env_id);
            const response_content = await response.json();
            envs[env_id] = new Set(response_content['agents']);
        }
        store.dispatch(create_environment({envs: envs}));
    }

    render() {
        let simulation_area = null;
        const simulated = this.state.env_type === 'Simulated';
        if(simulated)
            simulation_area = <Simulation/>;

        let env_sections = [];
        for(let id in this.state.environments)
            env_sections.push(<Environment key={`env_${id}`} id={`env_${id}`} env_id={id}/>);

        return <div>
                 <header>
                   <h2> Running {this.state.env_type} Environment </h2>
                 </header>
                 <main>
                   {env_sections}
                   <Relationship simulated={simulated}/>
                   {simulation_area}
                   <br/>
                   <textarea id="action_response" placeholder="REST API response here" readOnly={true} rows="3" cols="100"></textarea>
                 </main>
                 <footer>
                   <p> ARPS version {this.state.version} </p>
                 </footer>
               </div>;
    }
}

class Environment extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <section id={this.props.id}>
                 <h3>Environment ID: {this.props.env_id} </h3>
                 <Actions env_id={this.props.env_id}/>
               </section>;
    }
}

class Actions extends React.Component {

    constructor(props) {
        super(props);

        this.list = this.list.bind(this);
        this.retrive_monitor_logs = this.retrive_monitor_logs.bind(this);
        this.show_context_menu = this.show_context_menu.bind(this);
    }

    async list() {
        await execute_action_with_feedback(list_agents.bind(null, this.props.env_id));
    }

    async retrive_monitor_logs() {
        return await monitor_logs(this.props.env_id);
    }

    show_context_menu(action_name) {
        let context_menus = new Set(['spawn', 'status', 'terminate']);
        context_menus.delete(action_name);

        //enable current action context menu
        let element = document.getElementById(`${action_name}-${this.props.env_id}`);
        element.classList.remove('hidden');

        //disable the others context menu
        for(let context_menu of context_menus )
        {
            hide_element(`${context_menu}-${this.props.env_id}`);
        }
    }

    render() {
        const env_id = this.props.env_id;

        return <section id={env_id}>
                 <h4> Agent Actions </h4>
                 <button id={`list-action-${env_id}`} onClick={this.list}>List</button>
                 <button id={`spawn-action-${env_id}`} onClick={() => {this.show_context_menu('spawn');}}>Spawn</button>
                 <button id={`status-action-${env_id}`} onClick={() => {this.show_context_menu('status');}}>Status</button>
                 <button id={`terminate-action-${env_id}`} onClick={() => {this.show_context_menu('terminate');}}>Terminate</button>
                 <button id={`monitor-logs-action-${env_id}`} onClick={wrap_sim_action_blob(this.retrive_monitor_logs
)}>Monitor Logs</button>
                 <SpawnAction env_id={env_id}/>
                 <StatusAction env_id={env_id}/>
                 <TerminateAction env_id={env_id}/>
               </section>;
    }
}

class SpawnAction extends React.Component {
    constructor(props) {
        super(props);
        this.state = { policies: null, n: -1, loaded_policies: null};
        this.addPolicy = this.addPolicy.bind(this);
        this.removePolicy = this.removePolicy.bind(this);
        this.spawnAgent = this.spawnAgent.bind(this);
        this.initialState = this.initialState.bind(this);
    }

    async componentDidMount() {
        this.setState({policies: await list_policies(this.props.env_id)});
        this.initialState();
    }

    initialState() {
        let initial_policy = <PolicySelector env_id={this.props.env_id} selector_id={0} policies={this.state.policies} key={0}/>;
        this.setState({n: 0, loaded_policies: [initial_policy]});
    }

    addPolicy() {
        let n = this.state.n + 1;
        let initial_policy = <PolicySelector env_id={this.props.env_id} selector_id={n} policies={this.state.policies} key={n}/>;
        let loaded_policies = this.state.loaded_policies;
        loaded_policies.push(initial_policy);
        this.setState({n: n, loaded_policies: loaded_policies});
    }

    removePolicy() {
        let n = this.state.n - 1;
        let loaded_policies = this.state.loaded_policies;
        loaded_policies.pop();
        this.setState({n: n, loaded_policies: loaded_policies});
    }

    async spawnAgent() {
        const env_id = this.props.env_id;
        let policies = {};

        for(let loaded_policy in this.state.loaded_policies)
        {
            let v = document.getElementById(`policy-select-${env_id}-${loaded_policy}`);
            let policy_name = this.state.policies[v.selectedIndex];
            let is_periodic = document.getElementById(`periodic-${env_id}-${loaded_policy}`).checked;
            if(is_periodic) {
                let period = document.getElementById(`policy-period-${env_id}-${loaded_policy}`).value;
                policies[policy_name] = parseInt(period);
            } else {
                policies[policy_name] = null;
            }
        }
        const response = await spawn_agent(env_id, policies);
        if(response.status === 200) {
            let message = await response.json();
            const agent = message.split(' ')[1];
            store.dispatch(add_agent({env_id: env_id, agent: agent}));
            update_status_area(message, true);
        } else {
            update_status_area(response.statusText, false);
        }

        this.initialState();

        hide_element(`spawn-${env_id}`);
    }

    render() {
        const env_id = this.props.env_id;
        const disable = this.state.loaded_policies && this.state.loaded_policies.length === 1;

        return <section id={`spawn-${env_id}`} className="hidden spawn">
                 <div id={`policy-selector-${env_id}`}>
                   {this.state.loaded_policies}
                 </div>
                 <button id={`spawn-add-${env_id}`} onClick={this.addPolicy}>Add policy</button>
                 <button id={`spawn-remove-${env_id}`} onClick={this.removePolicy} disabled={disable}>Remove policy</button>
                 <button id={`spawn-ok-${env_id}`} onClick={this.spawnAgent}>Ok</button>
                 <button id={`spawn-cancel-${env_id}`} onClick={() => hide_element(`spawn-${env_id}`)}>Cancel</button>
               </section>;
    }
}

class StatusAction extends React.Component {
    constructor(props) {
        super(props);
        this.state = {agents : new Set(), sim_running: false};
        store.subscribe(() => {
            const state = store.getState();
            const agents = state.envs[this.props.env_id];
            this.setState({agents: new Set(agents)});
        });

        //It's ok to subscribe to sim_store in real environment. After
        //all, this is never going to be called.
        sim_store.subscribe(() => {
            const state = sim_store.getState();
            this.setState({sim_running: state.running});
        });

        this.agentStatus = this.agentStatus.bind(this);
    }

    async agentStatus() {
        const env_id = this.props.env_id;
        const request_type = document.getElementById(`status-request-select-${env_id}`).value;
        const agent = document.getElementById(`status-agent-select-${env_id}`).value;
        await execute_action_with_feedback(agent_status.bind(null, env_id, agent, request_type));
    }

    render() {
        const env_id = this.props.env_id;

        let element = document.getElementById(`status-action-${env_id}`);
        const disable = !this.state.sim_running || this.state.agents.size === 0;
        if(element) {
            element.disabled = disable;
            if(disable)
                hide_element(`status-${env_id}`);
        }

        let agents = [];
        for(let agent of this.state.agents) {
            agents.push(<option key={agent} value={agent}>{agent}</option>);
        }

        return <section id={`status-${env_id}`} className="hidden status">
                 <label htmlFor={`status-request-select-${env_id}`}>Policy</label>
                 <select id={`status-request-select-${env_id}`}>
                   <option value="info">Info</option>
                   <option value="sensors">Sensors</option>
                   <option value="actuators">Actuators</option>
                 </select>
                 <label htmlFor={`status-agent-select-${env_id}`}>Agent ID</label>
                 <select id={`status-agent-select-${env_id}`}>
                   {agents}
                 </select>
                 <button id={`status-ok-${env_id}`} onClick={this.agentStatus}>Ok</button>
                 <button id={`status-cancel-${env_id}`} onClick={() => hide_element(`status-${env_id}`)}>Cancel</button>
               </section>;
    }
}

class TerminateAction extends React.Component {
    constructor(props) {
        super(props);
        this.state = { agents: []};
        this.terminateAgent = this.terminateAgent.bind(this);
        store.subscribe(() => {
            const state = store.getState();
            const agents = state.envs[this.props.env_id];
            this.setState({agents: agents});
        });
    }

    async terminateAgent() {
        let message = "";
        let agents_to_remove = [];
        for(let agent of this.state.agents) {
            const element = document.getElementById(`agent-to-terminate-${agent}`);
            if(!element.checked)
                continue;

            let response = await terminate_agent(this.props.env_id, agent);
            const response_content = await response.json();
            message += response_content + "\r\n";
            if(response.status == 200) {
                agents_to_remove.push(agent);
            }
        };

        store.dispatch(remove_agents({env_id: this.props.env_id, agents: agents_to_remove}));

        update_status_area(message, true);

        hide_element(`terminate-${this.props.env_id}`);
    }

    render() {
        let element = document.getElementById(`terminate-action-${this.props.env_id}`);
        if(element)
            element.disabled = this.state.agents.size === 0;

        const env_id = this.props.env_id;

        let agents_for_termination = [];
        for(let agent of this.state.agents) {
            agents_for_termination.push(
                <div key={agent}>
                  <label htmlFor={`agent-to-terminate-${agent}`}>{agent}</label>
                  <input type="checkbox" id={`agent-to-terminate-${agent}`}/>
                </div>);
        };

        return <section id={`terminate-${env_id}`} className="hidden terminate">
                 <div id={`terminate-agents-${env_id}`}>
                   {agents_for_termination}
                 </div>
                 <button id={`terminate-ok-${env_id}`} onClick={this.terminateAgent}>Ok</button>
                 <button id={`terminate-cancel-${env_id}`} onClick={() => hide_element(`terminate-${env_id}`)}>Cancel</button>
               </section>;
    }
}

class PolicySelector extends React.Component {
    constructor(props) {
        super(props);
        this.state = {frequency: 1};
    }

    render() {
        const frequency_handler = (e) =>  {
            const new_value = e.target.value;
            if (new_value >= 1) {
                this.setState({frequency: new_value});
            }
        };

        let options = [];
        const policies = this.props.policies;
        for(let i in policies) {
            options.push(<option key={i}>{policies[i]}</option>);
        };

        const env_id = this.props.env_id;
        const selector_id = this.props.selector_id;

        return <div id={`policy-selector-${env_id}-${selector_id}`} className="policy-selector">
                 <label htmlFor={`policy-select-${env_id}-${selector_id}`}>Policy</label>
                 <select id={`policy-select-${env_id}-${selector_id}`}>
                   ${options}
                 </select>
                 <label htmlFor={`periodic-${env_id}-${selector_id}`}>Periodic</label>
                 <input type="checkbox" id={`periodic-${env_id}-${selector_id}`}/>
                 <label htmlFor={`policy-period-${env_id}-${selector_id}`}>Policy frequency (seconds)</label>
                 <input type="number" id={`policy-period-${env_id}-${selector_id}`} value={this.state.frequency} onChange={frequency_handler}/>
               </div>;
    }
}

class Relationship extends React.Component {
    constructor(props) {
        super(props);
        this.state = {agents : new Set()};
        this.updateAgentsRelationship = this.updateAgentsRelationship.bind(this);

        store.subscribe(() => {
            const state = store.getState();
            let all_agents = new Set();
            for(let agents in state.envs) {
                for(let agent of state.envs[agents]) {
                    all_agents.add(agent);
                }
            }
            this.setState({agents: all_agents});
        });
    }

    async updateAgentsRelationship() {
        const sim_state = sim_store.getState();
        if(this.props.simulated && !sim_state.running) {
            update_status_area('Simulation not running');
            return;
        }

        const agent_from = document.getElementById(`update-relationship-select-from`).value;
        const agent_to = document.getElementById(`update-relationship-select-to`).value;
        const operation = document.getElementById(`update-relationship-select-op`).value;

        const separator = agent_to.indexOf('.');
        const env_id = agent_to.slice(0, separator);
        await execute_action_with_feedback(update_agent_relationship.bind(null, env_id, agent_from, agent_to, operation));
    }

    render() {
        let agents_option = [];
        for(let agent of this.state.agents)
            agents_option.push(<option key={agent}>{agent}</option>);

        let className = 'update-relationship';
        if(this.state.agents.size < 2)
            className += ' hidden';

        return <section id={'update-relationship'} className={className}>
                 <h3>Agents relationship</h3>
                 <select id={'update-relationship-select-from'}>
                   {agents_option}
                 </select>
                 <select id={'update-relationship-select-op'}>
                   <option value='add'>Add</option>
                   <option value='remove'>Remove</option>
                 </select>
                 <select id={'update-relationship-select-to'}>
                   {agents_option}
                 </select>
                 <button id={'update-relationship-action-ok'} onClick={this.updateAgentsRelationship}>Ok</button>
               </section>;
    }
}

class Simulation extends React.Component {
    constructor(props) {
        super(props);
        this.run_sim = this.run_sim.bind(this);
        this.stop_sim = this.stop_sim.bind(this);
    }

    async componentDidMount() {
        const status = await sim_status();
        const status_content = await status.json();
        if(status_content === 'stopped')
            sim_store.dispatch(stop_simulation());
        else if(status_content === 'running')
            sim_store.dispatch(run_simulation());
        else
            console.log('Invalid response. Doing nothing');
    }

    async run_sim() {
        sim_store.dispatch(run_simulation());
        await execute_action_with_feedback(sim_run);
    }

    async stop_sim() {
        sim_store.dispatch(stop_simulation());
        await execute_action_with_feedback(sim_stop);
    }

    render() {
        return <div>
                 <section id="sim-actions">
                   <h3>Simulation action</h3>
                   <button id={`sim-run`} onClick={this.run_sim}>Run</button>
                   <button id={`sim-status`} onClick={execute_action_with_feedback.bind(null, sim_status)}>Status</button>
                   <button id={`sim-stop`} onClick={this.stop_sim}>Stop</button>
                   <button id={`sim-result`} onClick={wrap_sim_action_blob(sim_result)} disabled={false}>Result</button>
                   <button id={`sim-save`} onClick={execute_action_with_feedback.bind(null, sim_save)}>Environment State</button>
                   <button id={`sim-stats`} onClick={execute_action_with_feedback.bind(null, sim_stats)}>Stats</button>
                 </section>
               </div>;
    }
};

const hide_element = (element_id) => {
    let element = document.getElementById(`${element_id}`);
    if(element)
        element.classList.add('hidden');
};

const wrap_sim_action_blob = (action) => {
    return async() => {
        const response = await action();
        if(response.status !== 200)
        {
            update_status_area(response.statusText, false);
            return;
        }

        console.log(response.headers);
        const content_disposition = response.headers.get('content-disposition');
        console.log(content_disposition);
        const result_file = await response.blob();
        let blob = new Blob([result_file], {
            type: response.headers.get('content-type')
        });
        var file_url = URL.createObjectURL(blob);
        var anchor = document.createElement('a');

        anchor.href = file_url;
        anchor.target = '_blank';

        const filename = 'filename=';
        const start_index = content_disposition.indexOf(filename) + filename.length;
        anchor.download = content_disposition.substring(start_index);
        anchor.style = "display: none";

        document.body.appendChild(anchor);
        anchor.click();

        setTimeout(function() {
            document.body.removeChild(anchor);
        }, 100);
    };
};

const execute_action_with_feedback = async (action) => {
    const response = await action();
    if(response.status === 200) {
        const message = await response.json();
        update_status_area(JSON.stringify(message), true);
    } else {
        console.log(response);
        update_status_area(response.statusText, false);
    }
};

const update_status_area = (message, successful) => {

    let action_response = document.getElementById("action_response");
    if (!successful) {
        action_response.value = `Operation failed: ${message}`;
        return;
    }

    action_response.value = message;
};

let body = document.getElementById('root');
ReactDOM.render(<App />, body);
