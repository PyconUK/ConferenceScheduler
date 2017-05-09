Contributing
############

Contributions are welcome and much appreciated!

Development
-----------

To setup `ConferenceScheduler` for local development:

1. Fork the repository on Github `<https://github.com/https://github.com/PyconUK/ConferenceScheduler/fork>`_
2. Clone your fork to your local machine::

    git clone git@github.com:your_name_here/ConferenceScheduler.git

3. Create a branch for your work::

    git checkout -b name-of-your-branch

4. Commit your changes and push your branch to Github::

    git add -A
    git commit -m "A description of your changes"
    git push origin name-of-your-branch

5. Create a Pull Request at `<https://github.com/PyconUK/ConferenceScheduler/pulls>`_


Testing
-------

The library includes a comprehensive test suite. Please ensure that you run all the tests before submitting
a Pull Request.

To setup your environment for testing the library:

1. Install the necessary Python libraries::

    pip install -r requirements.txt

2. Run the test suite::

    python setup.py test

This basic setup will run the tests within the `tests` directory, but there is also the possibility to run
the code contained with the documentation to ensure it still works and also to check the whole codebase for syntax and formatting problems. To do so, create a file named `pytest.ini` at the root of your local project folder and enter the following content::

    [pytest]
    testpaths = tests docs
    python_files =
        test_*.py
        *_test.py
        tests.py
    pep8ignore =
        resources.py E701
    addopts = --pep8 --doctest-glob='*.rst'

Now, when you run `python setup.py test` it will also run the doctests and pep8 checks.
