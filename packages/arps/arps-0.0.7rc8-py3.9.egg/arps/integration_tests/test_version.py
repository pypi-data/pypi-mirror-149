import subprocess

import pytest # type: ignore

from arps import __version__ as arps_version


def test_versions():
    expected = f'ARPS {arps_version}\n'

    assert expected.encode() == subprocess.check_output(['agents_directory', '--version'])
    assert expected.encode() == subprocess.check_output(['agent_manager_runner', '--version'])
    assert expected.encode() == subprocess.check_output(['agent_runner', '--version'])
    assert expected.encode() == subprocess.check_output(['agent_client', '--version'])


if __name__ == '__main__':
    pytest.main([__file__])
