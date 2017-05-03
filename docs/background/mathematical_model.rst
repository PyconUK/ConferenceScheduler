Mathematical model
==================

The scheduler work by solving a well understood mathematical problem called an
integer linear program.

If we assume that we have :math:`M` events and :math:`N` slots, then
the schedule is mathematically represented by a binary matrix :math:`X\in\{0,
1\}^{M\times N}`. Every row corresponds to an event and every column to a slot:

.. math::
   :label: variable

   X_{ij} =
   \begin{cases}
       1,&\text{ if event }i\text{ is scheduled in slot }j\\
       0,&\text{otherwise}
   \end{cases}

From that we can build up various constraints on what is a valid schedule.


All events must be scheduled
----------------------------

For every row (event), we sum over every column of :math:`X` and must have total
sum 1.

.. math::
   :label: all_events_scheduled

   \sum_{j=1}^{N} X_{ij} = 1\text{ for all }1\leq i\leq M


All slots cannot have more than one event
-----------------------------------------

For every column (slot), we sum over every row of :math:`X` and must have total
sum at most 1.

.. math::
   :label: all_slots_at_most_1_event

   \sum_{i=1}^{M} X_{ij} \leq 1\text{ for all }1\leq j\leq N


This in itself would give a basic schedule for a conference however things can
be a bit more complicated:

- Some slots can be in parallel with each other (for example because of multiple
  rooms);
- Slots and events might have different duration;
- It might be desirable to have some common thread for talks in a collections of
  slots (for example: the morning session)

The mathematical representation for these constraints will be described below.

TBD
