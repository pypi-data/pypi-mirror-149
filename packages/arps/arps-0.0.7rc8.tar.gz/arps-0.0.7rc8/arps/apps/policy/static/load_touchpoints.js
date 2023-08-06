//TODO: create tickets for the todos below
//TODO: dynamic agents_directory configuration file
//TODO: agents_directory should return also the port where the agent manager is listening
//TODO: see headers={'Access-Control-Allow-Origin':'*'}. This is a security concern that should be address in the future (hostnames instead of *)

function load_touchpoints() {
    var sensors = [];
    var actuators = [];

    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200) {
	    document.getElementById("agents_directory_status").innerHTML = 'Agents Directory: Ok'

	    var response = JSON.parse(request.response).message;

	    if(Object.keys(response).length == 0 && response.constructor == Object) {
		document.getElementById("am_fetched").innerHTML = 'Agent Managers: No Agent Manager found'
		return
	    }

	    var send_request = function() {
		var url = 'http://' + response[agent_manager].address + ':' + 5000 + '/loaded_touchpoints';
		var promise = new Promise(function(resolve, reject) {
		    var resources_request = new XMLHttpRequest();
		    resources_request.onreadystatechange = function() {
			if (resources_request.readyState == 4 && resources_request.status == 200) {
			    var response = JSON.parse(resources_request.response).message
			    console.log(response)
			    sensors.push.apply(sensors, response.sensors)
			    actuators.push.apply(actuators, response.actuators)
			    resolve();
			}
			//FIXME not covering when it fails.
		    }
		    resources_request.open('GET', url, true);
		    resources_request.send(null);
		});
		return promise;
	    }

	    var promises = [];
	    for(var agent_manager in response) {
		promises.push(send_request());
	    }

	    Promise.all(promises).then(function() {
		var agent_managers_fetched = 'Agent Managers: '
		agent_managers_fetched = agent_managers_fetched.concat(Object.keys(response))
		document.getElementById("am_fetched").innerHTML = agent_managers_fetched

		console.log(sensors);
		console.log(actuators);
		load(sensors, "sensors");
		load(actuators, "actuators");
	    });
	} else if(request.readyState == 4 && request.status != 200) {
	    document.getElementById("agents_directory_status").innerHTML = 'Agents Directory: No response'
	}
    }

    //    agents_directory = JSON.parse('agents_directory_config.json');
    agents_directory = {"ad_address": "localhost", "ad_port": 1500}
    var url = 'http://' + agents_directory['ad_address'] + ':' + agents_directory['ad_port'] + '/list'
    request.open('GET', url, true);
    request.send(null)
}

function load(touchpoints, id) {
    var options = '<option> ' + touchpoints[0] + '</option>';
    for(var i = 1; i < touchpoints.length; i++)
	options += '<option>' + touchpoints[i] + '</option>';
    document.getElementById(id).innerHTML = options;
}
