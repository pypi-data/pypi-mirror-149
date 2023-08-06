import shutil

def check_for_apps():
    expected_apps = ['agents_directory', 'agent_runner', 'agent_manager_runner', 'pmt_service', 'sim_result_to_image']
    apps_available = all(shutil.which(expected_app) is not None for expected_app in expected_apps)
    if apps_available:
        return apps_available, 'All apps are available in the PATH'

    return apps_available, 'ARPS package configuration error: Verify if arps package is installed, if the environment variable PATH contains the apps, or if the virtual environment where the packge is, is active'
