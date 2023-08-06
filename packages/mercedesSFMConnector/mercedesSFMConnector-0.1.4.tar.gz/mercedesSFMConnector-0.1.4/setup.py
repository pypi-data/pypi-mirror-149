from setuptools import find_packages, setup
setup(
    name='mercedesSFMConnector',
    packages=find_packages(include=['mercedesSFMConnector', 'mercedesSFMConnector.api', 'mercedesSFMConnector.token_handler']),
    version='0.1.4',
    description='A library to interact with the Mercedes SFM API in Python',
    author='Ethan Wilkes',
    install_requires=['requests', 'requests-oauthlib','oauthlib'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    license='MIT',
)
