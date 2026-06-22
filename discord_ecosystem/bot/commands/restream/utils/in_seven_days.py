import time


def does_it_happen_within_a_week(timestamp: int):
    return int(time.time()) < timestamp < int(time.time() + 604800)
