from setuptools import setup, find_packages


setup(
    name='conference-scheduler',
    version='2.1.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
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
