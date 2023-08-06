function post() {
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/post");

    var policy = build_policy()

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "policy");
    hiddenField.setAttribute("value", policy);

    form.appendChild(hiddenField);

    document.body.appendChild(form);
    form.submit();
}

function build_policy() {
    var policy_name = document.getElementById("policy_name").value;
    var policy_description = document.getElementById("policy_description").value;
    var selected_sensor = selected("sensors");
    var selected_operator = operator(document.getElementById("operator").selectedIndex);
    var threshold = document.getElementById("sensor_threshold").value;

    var selected_actuator = selected("actuators");
    var action_value = document.getElementById("actuator_action").value;

    var policy = new Object();
    policy.name = policy_name;
    policy.description = policy_description;
    policy.sensor = selected_sensor;
    policy.operator = selected_operator;
    policy.threshold = threshold;
    policy.actuator = selected_actuator;
    policy.action = action_value;

    return JSON.stringify(policy);
}

function selected(id) {
    var selected = document.getElementById(id);
    var selected_index = selected.selectedIndex;
    return selected[selected_index].value;
}

function operator(op_code) {
    var operators = new Array();
    operators[0] = "gt";
    operators[1] = "ge";
    operators[2] = "eq";
    operators[3] = "ne";
    operators[4] = "le";
    operators[5] = "lt";

    return operators[op_code];
}
