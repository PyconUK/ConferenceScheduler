import numpy as np

def element_from_neighbourhood(X):
    """
    Randomly move an event:

    - Either to an empty slot
    - Swapping with another event
    """

    m, n = X.shape
    new_X = np.copy(X)

    event_to_move = np.random.randint(m)
    current_event_slot = np.where(new_X[event_to_move, :] == 1)[0][0]

    slot_to_move_to = np.random.randint(n - 1)
    if slot_to_move_to >= current_event_slot:
        slot_to_move_to += 1
    scheduled_events_in_slot = np.where(new_X[:, slot_to_move_to] == 1)[0]

    if len(scheduled_events_in_slot) == 0:  # No event in that slot
        new_X[event_to_move] = np.zeros(n)
        new_X[event_to_move, slot_to_move_to] = 1

    else: # There is an event in that slot
        swap_rows = [event_to_move, scheduled_events_in_slot[0]]
        new_X[swap_rows] = new_X[swap_rows[::-1]]

    return new_X

def get_initial_array(events, slots, seed=None):
    """
    Obtain a random initial array.
    """
    if seed is not None:
        np.random.seed(seed)

    m = len(events)
    n = len(slots)
    X = np.zeros((m, n))
    for i, row in enumerate(X):
        X[i, i] = 1
    np.random.shuffle(X)
    return X
