Use different solvers
=====================

The `Pulp <https://pythonhosted.org/PuLP/index.html>`_ library is a Python
interface to underlying solution engines. By default it comes packaged with `CBC
<https://projects.coin-or.org/Cbc>`_

It is however possible to use a number of other solvers (see the Pulp
documentation for details) and these can be passed to the scheduler. For example
here is how we would use the `GLPK <https://www.gnu.org/software/glpk/>`_
solver for a given set of :code:`events` and :code:`slots`::

    >>> scheduler.schedule(events=events, slots=slots, solver=pulp.GLPK()) # doctest: +SKIP

Different solvers can have major impact on the performance of the scheduler.
This can be an important consideration when scheduling large or highly
constrained problems.
