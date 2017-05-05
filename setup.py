from setuptools import setup

setup(
    name='conference-scheduler',
    version='1.0.0',
    packages=[
        'conference_scheduler',
    ],
    url='https://github.com/PyconUK/ConferenceScheduler',
    license='MIT',
    author='Owen Campbell, Vince Knight',
    author_email='owen.campbell@tanti.org.uk',
    description='A Python tool to assist the task of scheduling a conference',
    install_requires=['pulp', 'numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-pep8'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
)
