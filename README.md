# Conference Scheduler

# Overview
A Python tool to assist the task of scheduling a conference which:
* Can take an existing schedule and validate it against a set of constraints
* Can calculate a new schedule optimised to be the minimum change necessary from another given schedule
* Has the resources, constraints and optimisations defined below already built in
* Has a simple mechanism for defining new constraints and optimisations
* Is a standalone tool which takes simple data types as input and produces simple data types as output (i.e. does no IO or presentation)

# Resources
* Rooms - which have a maximum capacity
* Time slots - which have a start and end time
* Sessions - which define an ordered series of time slots (e.g. 'the session between coffee and lunch on Friday')
* Days - which contain an ordered series of sessions
* People - who have names
* Roles - e.g. 'Speaker', 'Session Chair', 'Mentor'
* Unavailability - Time slots for which a person is not available to fulfil a role
* Events - which might be talks or workshops and may have a classification
* Demand - the predicted size of audience for an event

# Built-In Constraints
* A room may only have a maximum of one event scheduled in any time slot
* An event may only be scheduled in one combination of room and time slot
* An event has at least one defined role, none of which may be 'Session Chair'
* A person may only perform one role in any time slot except for 'Mentor' which is allowed alongside any other role
* A person must not be scheduled to fulfil a role in a time slot for which they are unavailable
* Any person assigned the 'Session Chair' role must not be assigned any other role in the same session
* No person must be scheduled to chair more sessions than they have specified themselves nor the maximum number defined for the conference

# Optimisation
* The sum of 'potential disappointments' should be minimised where 'potential disappointments' is defined as the excess of demand over room capacity for every scheduled event
* The number of time slot/room combinations without a person assigned to the 'Session chair' role should be minimised
* The number of occasions where the session chair changes for the time slots within a session for any room should be minimised

# Ad-Hoc Constraints and Optimisations
Some examples of situations which have arisen at previous conferences and should be handled by defining ad-hoc constraints or optimisations:
* A conference organiser says "Talks X and Y are on similar subject matter and likely to appeal to a similar audience. Let's try not to schedule them against each other."
* A conference organiser says "Talks X, Y and Z are likely to appeal to a similar audience. Let's try to schedule them sequentially in the same room so that we minimise the movement of people from one room to another."
* A conference organsier says "The audience for Talk X would benefit greatly from the speech-to-text provision. Let's schedule that one in the main hall."
* A potential session chair says "I'd like to attend workshop X, so please don't schedule me to chair a session that clashes with it."
* A potential session chair says "I'm happy to chair a session but I've never done it before, so please don't schedule me in the main hall."
* A speaker says "I'd like to attend talk X, so please don't schedule my talk in the same slot."
* A first-time speaker is assigned a mentor and requests that the mentor chairs the session in which they are scheduled to give their talk.
