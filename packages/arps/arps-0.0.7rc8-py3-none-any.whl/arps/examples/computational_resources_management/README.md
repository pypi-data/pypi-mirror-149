Simple example showing some of the ARPS framework capabilities
============

# Requirements

	* GNU Linux

	* powertop tool: https://01.org/powertop

# QuickStart (Linux)

	* After getting the example, initialize the virtual environment

	```
	cd example_folder
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -e .
	```

	* Run the MAS in simulator mode
   ```
   agent_manager_runner --config_file conf/simulator.conf
   ```

	* Run the MAS in actual mode.

		1. Open a new terminal, go the example folder and activate the virtual environment
		```
		agents_directory
		```

		2. In the original terminal, run:
		```
		agent_manager_runner --config_file conf/real.conf
		```
