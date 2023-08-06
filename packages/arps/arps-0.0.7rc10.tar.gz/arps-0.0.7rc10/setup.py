from setuptools import find_packages, setup

requirements = [
    'aiohttp==3.7.4',
    'aiohttp_debugtoolbar',
    'aiohttp_jinja2>=1.5',
    'psutil>=5.9.0',
    'pytest>=7.1.2',
    'pytest-xdist>=2.5.0',
    'pytest-asyncio>=0.18.3',
    'python-dateutil',
    'gevent>=21.12.0',
    'parse>=1.19.0',
    'pre-commit',
    'simplejson>=3.17.6',
    'tinydb>=4.7.0',
    'matplotlib>=3.2.1',
    'pandas>=1.3.5',
]

with open('VERSION') as version_file:
    version = version_file.read()

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='arps',
    python_requires='>3.7.0, <3.10.0',
    version=version,
    description=('Multi-Agent System framework for managing resource with simulator for self-evaluation'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/arps/arps',
    license='MIT',
    author='Thiago Coelho Prado',
    author_email='coelhudo@gmail.com',
    packages=find_packages(exclude=['*tests*']),
    package_data={'arps': ['py.typed']},
    install_requires=requirements,
    platforms='any',
    entry_points='''
      [console_scripts]
      agents_directory=arps.apps.agents_directory:main
      agent_manager_runner=arps.apps.agent_manager_runner:main
      agent_runner=arps.apps.agent_runner:main
      pmt_service=arps.apps.policy.main:main
      sim_result_to_image=arps.apps.event_log_parser:main
      agent_client=arps.apps.client:main
      ''',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
