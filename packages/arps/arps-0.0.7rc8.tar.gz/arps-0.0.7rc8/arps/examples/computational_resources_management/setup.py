from setuptools import find_packages, setup

requirements = ['arps==0.0.6.rc1']

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(name='arps_example',
      python_requires='>3.7.0',
      description=('Example to show how the ARPS framework can be used'),
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitlab.com/arps/arps',
      license='MIT',
      author='Thiago Coelho Prado',
      author_email='coelhudo@gmail.com',
      packages=find_packages(),
      install_requires=requirements,
      platforms='any',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
      ]
      )
