import discord
import copy


class MatchState():

    def __init__(self,
                 main_channel: discord.TextChannel,
                 thread: discord.Thread,
                 player1: discord.Member,
                 player2: discord.Member,
                 categories: dict,
                 nb_bans: int = 1,
                 nb_picks: int = 1,
                 nb_matches: int = 2,
                 keep_category: bool = True):
        self.available_choices = copy.deepcopy(categories)
        self.players = [player1, player2]
        self.bans = []
        self.picks = []
        self.nb_bans = nb_bans
        self.nb_picks = nb_picks
        self.nb_matches = nb_matches
        self.keep_category = keep_category
        self.matches: list[tuple[str, discord.Member | None]] = []
        self.main_channel = main_channel,
        self.thread = thread

    def ban(self, choice: str):
        if choice in self.available_choices.keys():
            del self.available_choices[choice]
        self.bans.append(choice)

    def pick(self, category: str, mode: str):
        if self.keep_category:
            self.available_choices[category].remove(mode)
        else:
            del self.available_choices[category]
        self.picks.append(mode)

    def get_current_state(self):
        if len(self.bans) < 2 * self.nb_bans:
            return "ban", len(self.bans) % 2
        if len(self.picks) < 2 * self.nb_picks:
            return "pick", len(self.picks) % 2
        if len(self.picks) < self.nb_matches:
            return "generate_matches", None
        return None, None
