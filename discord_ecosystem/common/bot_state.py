from enum import Enum


class TournamentStatesEnum(Enum):
    """
        INITIAL_STATE : no tournament is happening
            -> go to VALIDATING
        VALIDATING: we're currently checking the config
            -> go to CREATING_STRUCTURE
        CREATING_STRUCTURE: we're creating the channels, assigning the roles, etc.
            -> go to GAME_PHASE
        GAME_PHASE: we're currently in pick / ban / match phase
            -> we can receive the set_result command, we can go to RESULT_PHASE
               when we have all results
        RESULT_PHASE: we've all results for the current phase
            -> we can either go back to INITIAL_PHASE (tournament finished),
               or to GAME_PHASE (next round)
    """
    INITIAL_STATE = 0
    VALIDATING = 1
    CREATING_STRUCTURE = 2
    GAME_PHASE = 3
    RESULT_PHASE = 4
    CLEANUP_PHASE = 5
    ERROR = 12


class TournamentsStates():

    current_tournaments = {}

    @classmethod
    def getTournamentState(cls, guild_id):
        if not cls.current_tournaments.get(guild_id, None):
            cls.current_tournaments[guild_id] = {
                "status": TournamentStatesEnum.INITIAL_STATE
            }
        return cls.current_tournaments[guild_id]

    @classmethod
    def update_status(cls, guild_id: int, status: TournamentStatesEnum):
        cls.getTournamentState(guild_id)["status"] = status

    @classmethod
    def get_status(cls, guild_id: int):
        return cls.getTournamentState(guild_id)["status"]

    @classmethod
    def store_config(cls, guild_id: int, config: dict):
        cls.getTournamentState(guild_id)["config"] = config


"""
    what does a tournament need to have, to get back on its feet after a shutdown.
    In general: GUILD
    INITIAL_STATE : nothing
    VALIDATING: we don't go back from here, this state is just here to avoid spam
    CREATING_STRUCTURE: we need the config data
    GAME_PHASE: we need the groups and their matches / ban / pick already done
    RESULT_PHASE: we need the matches
"""
"""
    group :
        players: [],
        matches: [{
            player_1: ...
            player_2: ...
            pick_player_1: ...
            pick_player_2: ...
            ban_player_1: ...
            ban_player_2: ...
            match_results: [

            ]
        }]
"""
