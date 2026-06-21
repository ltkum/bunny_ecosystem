import time


def does_it_happen_in_a_week(timestamp: int):
    return timestamp < int(time.time() + 604800)
