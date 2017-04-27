from typing import Callable, List, Dict


def variables():
    """Defines the required instances of pulp.LpVariable

    Parameters
    ----------

    Returns
    -------
    dict
        mapping a meaningful reference to an instance of pulp.LpVariable
    """
    variables = {}
    return variables


class Constraint(NamedTuple):
    function: Callable
    args: List
    kwargs: Dict
    operator: Callable
    value: int
