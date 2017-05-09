.. _mathematical-model:

Mathematical model
==================


The scheduler works by solving a well understood mathematical problem called an
integer linear program [Dantzig1963]_, [Schaerf1999]_.

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

The constraints
+++++++++++++++


All events must be scheduled
----------------------------

For every row (event), we sum over every column of :math:`X` and must have total
sum 1.

.. math::
   :label: all_events_scheduled_constraint

   \sum_{j=1}^{N} X_{ij} = 1\text{ for all }1\leq i\leq M


All slots cannot have more than one event
-----------------------------------------

For every column (slot), we sum over every row of :math:`X` and must have total
sum at most 1.

.. math::
   :label: all_slots_at_most_1_event_constraint

   \sum_{i=1}^{M} X_{ij} \leq 1\text{ for all }1\leq j\leq N


This in itself would give a basic schedule for a conference however things can
be a bit more complicated:

- Some slots can be in parallel with each other (for example because of multiple
  rooms);
- Slots and events might have different duration;
- It might be desirable to have some common thread for talks in a collections of
  slots (for example: the morning session)

The mathematical representation for these constraints will be described below.

Events are only scheduled in slots for which they are available
---------------------------------------------------------------

There are multiple reasons for which an event might not be available in a given
slot: perhaps the speaker is unavailable on a given day.

These constraints can be captured using a matrix :math:`C_s\in\{0, 1\}^{M\times
N}`:

.. math::
   :label: slot_constraint_matrix

   {C_{s}}_{ij} =
   \begin{cases}
       1,&\text{ if event }i\text{ is available in slot }j\\
       0,&\text{otherwise}
   \end{cases}

This gives the following constraint:

.. math::
   :label: slot_constraint

    X_{ij} \leq {C_{s}}_{ij}\text{ for all }1\leq i\leq M,\,1\leq j\leq N

Two events are scheduled at the same time only if they are available to do so
-----------------------------------------------------------------------------

Any two given events might not be able to occur concurrently: two events could
be delivered by the same speaker, or they could be about a similar topic.

This constraint is captured using a matrix :math:`C_{e}\in\{0, 1\}^{M\times M}`:

.. math::
   :label: event_constraint_matrix

   {C_{e}}_{ii'} =
   \begin{cases}
       1,&\text{ if event }i\text{ is available during event }i'\\
       0,&\text{otherwise}
   \end{cases}

Using this, we define the following set for every slot :math:`j`:

.. math::
   :label: concurrent_slot_set

   S_j = \{1\leq j'\leq N\,|\,\text{ if }j\text{ and }j'\text{ are at the same time}\}

Using this we have the following constraint:

.. math::
   :label: event_constraint

    X_{ij}  + X_{i'j'} \leq 1 + {C_{e}}_{ii'}\text{ for all }j'\in S_j\text{ for all }1\leq j\leq N\text{ for all }1\leq i,i'\leq M

We see that if :math:`{C_{e}}_{ii'}=0` then at most one of the two events can be
scheduled across the two slots :math:`j,j'`.

Talks in a given session have something in common
-------------------------------------------------

It might be desirable to schedule collection of time slots in such a way that
the events in that collection have something in common. Perhaps all talks in a
morning session in a particular room should be welcoming to delegates of a given
level of expertise.

To do this we first need to capture each collection of slots into sessions, and
we define the following set for every slot :math:`j`:

.. math::
   :label: same_session_set

   {K}_{j} = \{1\leq j' \leq N\,|\,\text{ if }j\text{ and }j'\text{ are in the same session}\}

We also assume that we have a number of collections of events. Note that these
collections are non disjoint: any event can be in multiple collections. We refer
to these collections as "tags": an event can for example be tagged as
"beginner".

Using this we define the following set for every event :math:`i`

.. math::
   :label: same_tag_event_set

   T_i = \{1\leq i'\leq M\,|\,\text{ if }i\text{ and }j\text{ do not share a tag}\}

This leads us to the following constraint:

.. math::
   :label: tag_constraint

    X_{ij}  + X_{i'j'} \leq 1 \text{ for all  }j'\in K_j\text{ for all }1\leq j\leq N\text{ for all }i'\in T_i\text{ for all }1\leq i\leq M


Expressions :eq:`all_events_scheduled_constraint`,
:eq:`all_slots_at_most_1_event_constraint`,
:eq:`slot_constraint`, :eq:`event_constraint` and :eq:`tag_constraint` define a
valid schedule and can be used by themselves.

However, it might be desirable to also optimise a given objective function.

Objective functions
+++++++++++++++++++

Optimising to avoid room overflow
---------------------------------

Demand for events might be known: this will be captured using a vector
:math:`d\in\mathbb{R}_{\geq 0}^{M}`. Similarly capacity for rooms might be
known, captured using another vector :math:`c\in\mathbb{R}_{\geq 0}^{N}`. Whilst
it might not be possible to stick to those constraints strongly (when dealing
with parallel sessions delegates might not go where they originally intended) we
can aim to minimise the expected overflow given by the following expression:

.. math::
   :label: overflow_objective_function

   \sum_{i=1}^{M}\sum_{j=1}^{N}X_{ij}(c_j - d_i)

Using this, our optimisation problem to give a desirable schedule is obtained by
solving the following problem:

Minimise :eq:`overflow_objective_function` subject to :eq:`all_events_scheduled_constraint`,
:eq:`all_slots_at_most_1_event_constraint`,
:eq:`slot_constraint`, :eq:`event_constraint` and :eq:`tag_constraint`.

Minimise change from a previous schedule
----------------------------------------

Once a schedule has been obtained and publicised to all delegates, a new
constraint might arise (modifying :eq:`all_events_scheduled_constraint`,
:eq:`all_slots_at_most_1_event_constraint`,
:eq:`slot_constraint`, :eq:`event_constraint` and :eq:`tag_constraint`). At this
point the original optimisation problem can be solved again leading to a
potentially completely different schedule. An alternative to this is to use
distance from an original schedule :math:`X_o` as the objective function. Norms
on matrix spaces are usually non linear however, given the boolean nature of our
variables, the following function can be used to measure the number of changes:

.. math::
   :label: number_of_changes_objective_function

   \sum_{i=1}^{M}\sum_{j=1}^{N}\delta({X_o}_{ij}, X_{ij})

where :math:`\delta:\{0,1\}^{2}\to\{0,1\}` is given by:

.. math::
   :label: boolean_matrix_norm

   \delta(x_o, x) =
   \begin{cases}
       x,&\text{ if } x_o=0\\
       1-x,&\text{ if } x_o=1
   \end{cases}


Using this it is possible to obtain a schedule that is least disruptive from
another schedule when presented with new constraints by solving the following
problem:

Minimise :eq:`number_of_changes_objective_function` subject to
:eq:`all_events_scheduled_constraint`,
:eq:`all_slots_at_most_1_event_constraint`, :eq:`slot_constraint`,
:eq:`event_constraint` and :eq:`tag_constraint`.
