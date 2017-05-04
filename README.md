[![Coverage Status](https://coveralls.io/repos/github/PyconUK/ConferenceScheduler/badge.svg?branch=master)](https://coveralls.io/github/PyconUK/ConferenceScheduler?branch=master) [![Build Status](https://travis-ci.org/PyconUK/ConferenceScheduler.svg?branch=master)](https://travis-ci.org/PyconUK/ConferenceScheduler) [![Build status](https://ci.appveyor.com/api/projects/status/cvi70xoqqbwnwxdy?svg=true)](https://ci.appveyor.com/project/meatballs/conferencescheduler) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/db6b0af308a947d098c5f6205e2a90b4/badge.svg)](https://www.quantifiedcode.com/app/project/db6b0af308a947d098c5f6205e2a90b4)

# Conference Scheduler

# Overview
A Python tool to assist the task of scheduling a conference which:
* Can take an existing schedule and validate it against a set of constraints
* Can calculate a new valid, optimal schedule
* Can calculate a new, valid schedule also optimised to be the minimum change necessary from another given schedule
* Has the resources, constraints and optimisations defined below already built in
* Has a simple mechanism for defining new constraints and optimisations
* Is a standalone tool which takes simple data types as input and produces simple data types as output (i.e. does no IO or presentation)

# Terms
* Period - a period of time with defined start and end times
* Slot - a combination of room and period
* Session -  an ordered series of slots (e.g. 'the session in room 1 between coffee and lunch on Friday')
* People
* Role - e.g. 'Speaker', 'Session Chair', 'Mentor'
* Event - a talk or workshop
* Demand - the predicted size of audience for an event

# Built-In Constraints
* A slot may only have a maximum of one event scheduled
* A room may only be scheduled to host an event for which it is deemed suitable
* An event has at least one defined role, none of which may be 'Session Chair'
* A person may only perform one role in any time slot except for 'Mentor' which is allowed alongside any other role
* A person must not be scheduled to fulfil a role in a time slot for which they are unavailable
* Any person assigned the 'Session Chair' role must not be assigned any other role in the same session
* No person must be scheduled to chair more sessions than they have specified themselves nor the maximum number defined for the conference
* A workshop does not require a session chair

# Built-In Optimisations
* The sum of 'potential disappointments' should be minimised where 'potential disappointments' is defined as the excess of demand over room capacity for every scheduled event
* The number of slot/talk combinations without a person assigned to the 'Session chair' role should be minimised
* The number of occasions where the session chair changes within a session for any room should be minimised

# Ad-Hoc Constraints and Optimisations
Some examples of situations which have arisen at previous conferences and should be handled by defining ad-hoc constraints or optimisations:
* A conference organiser says "Talks X and Y are on similar subject matter and likely to appeal to a similar audience. Let's try not to schedule them against each other."
* A conference organiser says "Talks X, Y and Z are likely to appeal to a similar audience. Let's try to schedule them sequentially in the same room so that we minimise the movement of people from one room to another."
* A conference organsier says "The audience for Talk X would benefit greatly from the speech-to-text provision. Let's schedule that one in the main hall."
* A potential session chair says "I'd like to attend workshop X, so please don't schedule me to chair a session that clashes with it."
* A potential session chair says "I'm happy to chair a session but I've never done it before, so please don't schedule me in the main hall."
* A speaker says "I'd like to attend talk X, so please don't schedule my talk in the same slot."
* A first-time speaker is assigned a mentor and requests that the mentor chairs the session in which they are scheduled to give their talk.

# Acknowledgments
This repository was inspired by a talk given by David MacIver at PyCon UK 2016: http://2016.pyconuk.org/talks/easy-solutions-to-hard-problems/
