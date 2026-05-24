""" This will be used to store the various states for the application, and retrieve them from the database

What we need right now:

TOURNAMENT:
    NOT_RUNNING -> CREATING_GROUPS -> SENDING_GROUP_MATCHES -> WAITING_FOR_MATCHES_TO_END
    -> RESULTS -> BRACKET_PHASE -> SENDING_BRACKET_MATCHES -> WAITING_FOR_END -> LOOP OVER BRACKET PHASE UNTIL THERE IS NOT ENOUGH TEAM TO CONTINUE
    -> NOT RUNNING

    group phase might be skipped

MATCH:
    - PLAYER_1_BAN -> PLAYER_2_BAN -> PLAYER_1_PICK -> PLAYER_2_PICK -> MATCH_1_PLAYED -> MATCH_2_PLAYED -> ROULETTE -> MATCH_3_PLAYED -> RESULT
"""


class Tournament():

    state = None

    @classmethod
    def get_tournament_state(cls):
        return cls.state

    @classmethod
    def set_tournament_state(cls, state):
        cls.state = state

    @classmethod
    def is_tournament_ongoing(cls):
        return cls.state is not None
