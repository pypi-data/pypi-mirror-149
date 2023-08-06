# Installing from source #

```
user$ git clone https://www.gitlab.com/arps/arps.git
user$ cd arps
user$ python3 -m venv .venv
user$ pip3 install -e .
```

The _install_ option make pip command execute _setup.py_ script and _-e_ opntion will create a symbolic link to the project in the virtual environment. So, every time the code is edited the changes will be immediate.

# Running #

## Tests ##

Tests are executed using [pytest](https://docs.pytest.org/en/latest/).

```
user$ pytest
```

Or,

```
user$ pytest arps/integration_tests # for integration tests only
```

Three categories are available: arps/tests, arps/integration\_tests,
and arps/functional\_tests

See [pytest](https://docs.pytest.org/en/latest/) documentation for more information.

## Execution real world

* See: functional\_tests/test\_rest\_service to see how agents can be deployed

## Execution simulation

* See:
  * functional\_tests/test\_rest\_service: how agents are deployed
  * functional\_tests/test\_rest\_simulator: how the interaction to
  run as simulator works
  * functional\_tests/test\_rest\_simulator\_tools: how to generate
	charts from results

# Code

## Web GUI

Dependencies: npm

The web code is in arps/apps/web. The GUI is implemented using ReactJS.

When contributing to the code, execute `npm run build` to update the
code that will be executed in the browser.
