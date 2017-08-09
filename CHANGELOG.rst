Changelog
#########

v2.2.2 (2017-08-09)
-------------------
*  Bug Fixes: Heuristic algorithmss
   `#98 <https://github.com/PyconUK/ConferenceScheduler/pull/98>`_
   `#99 <https://github.com/PyconUK/ConferenceScheduler/pull/99>`_

v.2.1.1 (2017-08-08)
--------------------
*  Enhancement: ``scheduler.heuristic`` now returns in solution form
   `#97 <https://github.com/PyconUK/ConferenceScheduler/pull/97>`_

v2.1.0 (2017-08-08)
-------------------
*  New Feature: ``scheduler.heuristic`` uses a heuristic method rather than an
   integer linear programming approach

*  Enhancement: ``scheduler.array``, ``scheduler.schedule_to_array`` and
   ``scheduler.solution_to_array`` now return arrays of integers, not
   arrays of floats.
   `#94 <https://github.com/PyconUK/ConferenceScheduler/pull/94>`_

v2.0.0 (2017-05-12)
-------------------
*  Incompatibility: ``Event.tags`` and ``Event.unavailability`` are now immutable
   rather than list objects. List methods to update them will no longer work.

*  New Feature: Methods to add tags and unavailability to Event objects
   `#77 <https://github.com/PyconUK/ConferenceScheduler/pull/77>`_

*  Enhancement: the ``tags`` and ``availability`` arguments to ``Event`` are
   optional, and default to an empty list.
   `#74 <https://github.com/PyconUK/ConferenceScheduler/pull/74>`_

v1.2.0 (2017-05-09)
-------------------
*  Enhancement: Move source code and tests into separate directories and use pytest to run documentation tests
   `#72 <https://github.com/PyconUK/ConferenceScheduler/pull/72>`_

*  Enhancement: Schedules are now returned as lists rather than generator objects
   `#67 <https://github.com/PyconUK/ConferenceScheduler/pull/67>`_

*  Enhancement: Add the `bumpversion <https://pypi.python.org/pypi/bumpversion>`_ tool and its configuration
   `#65 <https://github.com/PyconUK/ConferenceScheduler/pull/65>`_

*  Enhancement: Use a more efficient summation function instead of plain
   addition within constraints
   `#64 <https://github.com/PyconUK/ConferenceScheduler/pull/64>`_

*  New Feature: Differences between schedules
   `#63 <https://github.com/PyconUK/ConferenceScheduler/pull/63>`_

*  Bug Fix: Unnecessary constraints were not being removed
   `#61 <https://github.com/PyconUK/ConferenceScheduler/pull/61>`_

v1.1.0 (2017-05-06)
-------------------

*  New Feature: Added the ability to pass different solver engines to
   the scheduler
   `#57 <https://github.com/PyconUK/ConferenceScheduler/pull/57>`_

*  Enhancement: Added a more efficient summation function in constraints
   `#55 <https://github.com/PyconUK/ConferenceScheduler/pull/55>`_

*  Enhancement: Removed the creation of unnecessary constraints
   `#54 <https://github.com/PyconUK/ConferenceScheduler/pull/54>`_

*  Enhancement: Altered the treatment of duration within constraints
   `#53 <https://github.com/PyconUK/ConferenceScheduler/pull/53>`_

*  Bug Fix: Package traversal in setup.py
   `#52 <https://github.com/PyconUK/ConferenceScheduler/pull/52>`_

v1.0.0 (2017-05-05)
-------------------

Initial release
