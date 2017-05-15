|Coverage Status| |Build Status| |Build status| |Code Issues|

Conference Scheduler
====================

Overview
========

A Python tool to assist the task of scheduling a conference which:

- Can take an existing schedule and validate it against a set of
  constraints
- Can calculate a new valid, optimal schedule
- Can calculate a new, valid schedule also optimised to be the minimum change
  necessary from another given schedule
- Has the resources, constraints and optimisations defined below built in
- Has a simple mechanism for defining new constraints and optimisations
- Is a standalone tool which takes simple data types as input and produces
  simple data types as output (i.e. does no IO or presentation)

The full documentation can be found at
`conference-scheduler.readthedocs.org <http://conference-scheduler.readthedocs.org/>`__.

Terms
=====

-  Slot - a combination of room and period
-  Session - an ordered series of slots (e.g. 'the session in room 1
   between coffee and lunch on Friday')
-  Event - a talk or workshop
-  Demand - the predicted size of audience for an event
-  Capacity - the capacity of venues

Constraints
===========

-  All events must be scheduled
-  A slot may only have a maximum of one event scheduled
-  An event must not be scheduled in a slot for which it has been marked
   as unavailable
-  An event must not be scheduled at the same time as another event for
   which it has been marked not to clash
-  An event may be tagged and, if so, must be scheduled in a session
   where it shares at least one tag with all other events in that
   session

Optimisation
============

Two options:

-  The sum of 'potential disappointments' should be minimised where
   'potential disappointments' is defined as the excess of demand over
   room capacity for every scheduled event
-  Minimise the number of changes from a given schedule.

Examples
========

Some examples of situations which have arisen at previous conferences
and could be handled by the unavailability, clashing and tagging
constraints:

- A conference organiser says "Talks X and Y are on similar subject matter and
  likely to appeal to a similar audience. Let's try not to schedule them
  against each other."
- A conference organiser says "Talks X, Y and Z are likely to appeal to a
  similar audience. Let's try to schedule them sequentially in the same room so
  that we minimise the movement of people from one room to another."
- A conference organiser says "The audience for Talk X would benefit greatly
  from the speech-to-text provision. Let's schedule that one in the main hall."
- A potential session chair says "I'd like to attend workshop X, so please
  don't schedule me to chair a session that clashes with it."
- A potential session chair says "I'm happy to chair a session but I've
  never done it before, so please don't schedule me in the main hall."
- A speaker says "I'd like to attend talk X, so please don't schedule my
  talk in the same slot."
- A first-time speaker is assigned a mentor and requests that the mentor chairs
  the session in which they are scheduled to give their talk.

Acknowledgements
================

This repository was inspired by a talk given by David MacIver at PyCon
UK 2016: http://2016.pyconuk.org/talks/easy-solutions-to-hard-problems/

.. |Coverage Status| image:: https://coveralls.io/repos/github/PyconUK/ConferenceScheduler/badge.svg?branch=master
   :target: https://coveralls.io/github/PyconUK/ConferenceScheduler?branch=master
.. |Build Status| image:: https://travis-ci.org/PyconUK/ConferenceScheduler.svg?branch=master
   :target: https://travis-ci.org/PyconUK/ConferenceScheduler
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/cvi70xoqqbwnwxdy?svg=true
   :target: https://ci.appveyor.com/project/meatballs/conferencescheduler
.. |Code Issues| image:: https://www.quantifiedcode.com/api/v1/project/db6b0af308a947d098c5f6205e2a90b4/badge.svg
   :target: https://www.quantifiedcode.com/app/project/db6b0af308a947d098c5f6205e2a90b4
