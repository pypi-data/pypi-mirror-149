const request_action = async(endpoint, resource, parameters, body, method) => {
    let url = `http://${endpoint}/${resource}`;
    if (parameters) {
	url += `?${parameters}`;
    }

    console.log(url);

    let message = {method: method};
    if (body) {
	message['body'] = JSON.stringify(body);
	message['headers'] = {
	    'Content-Type': 'application/json'
	};
    }
    return await fetch(url, message);
};

export {request_action};
