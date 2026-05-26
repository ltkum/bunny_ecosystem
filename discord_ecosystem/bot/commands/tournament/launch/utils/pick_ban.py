import copy
import discord

from bot.ui.views.options_select_view import SelectView

from bot.commands.tournament.launch.ui.pick_view import PickView

NO_BAN = "Je ne souhaite pas bannir de Catégorie"


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
        self.players = (player1, player2)
        self.bans = []
        self.picks = []
        self.nb_bans = nb_bans
        self.nb_picks = nb_picks
        self.nb_matches = nb_matches
        self.keep_category = keep_category
        self.matches: list[tuple[str, discord.Member | None]] = []
        self.main_channel = main_channel
        self.thread = thread

    def ban(self, choice: str | None):
        if choice and choice in self.available_choices.keys():
            del self.available_choices[choice]
        self.bans.append(choice)

    def pick(self, category: str, mode: str):
        if self.keep_category:
            del self.available_choices[category]["modes"][mode]
        else:
            del self.available_choices[category]
        self.picks.append(mode)

    def get_current_state(self):
        print(self.bans)
        print(self.picks)
        if len(self.bans) < 2 * self.nb_bans:
            return "ban", len(self.bans) % 2
        if len(self.picks) < 2 * self.nb_picks:
            return "pick", len(self.picks) % 2
        return "generate_matches", None


async def ask_ban(index: int, state: MatchState):
    view = SelectView(choices=[
        *[
            key for key in state.available_choices.keys()
            if state.available_choices[key]["bannable"]
            and not state.available_choices[key]["consent_required"]
        ], NO_BAN
    ],
                      callback_fn=ban_confirmed,
                      placeholder="Choisissez une catégorie à bannir",
                      state=state)
    await state.players[index].send(generate_ban_message(
        state.players[index], state.players[1 - index], state.bans),
                                    view=view,
                                    silent=True)


async def ban_confirmed(interaction: discord.Interaction, selected,
                        state: MatchState):

    if len(state.bans) % 2 != state.players.index(interaction.user) or len(
            state.bans) >= 2 * state.nb_bans:
        await interaction.response.send_message(
            "Ce n'est pas à votre tour de bannir", ephemeral=True)
        return
    await interaction.response.send_message(
        "Merci d'avoir effectué votre bannissement.")
    state.ban(selected if selected != NO_BAN else None)
    await check_next_instruction(state)


async def check_next_instruction(state: MatchState):
    phase, index_player = state.get_current_state()
    if phase == "ban":
        await ask_ban(index_player, state)
    elif phase == "pick":
        await ask_pick(index_player, state)
    elif phase == "generate_matches":
        await generate_matches(state)


async def ask_pick(index: int, state: MatchState):
    view = PickView(state.available_choices, state, pick_confirmed)
    await state.players[index].send(generate_pick_message(
        state.players[index], state.players[1 - index], state.picks),
                                    view=view,
                                    silent=True)


async def pick_confirmed(interaction: discord.Interaction, category, mode,
                         state: MatchState):
    if len(state.picks) % 2 != state.players.index(interaction.user) or len(
            state.picks) >= 2 * state.nb_picks:
        await interaction.response.send_message(
            "Ce n'est pas à votre tour de choisir", ephemeral=True)
        return
    await interaction.response.send_message(
        "Merci d'avoir effectué votre choix.", ephemeral=True)
    state.pick(category, mode)
    await check_next_instruction(state)


async def pick_ban_process(player1: discord.Member, player2: discord.Member,
                           result_channel: discord.TextChannel,
                           thread: discord.Thread, categories: dict, **kwargs):
    match = MatchState(result_channel, thread, player1, player2, categories, 1,
                       1, 2 + int(kwargs.get("third_match_needed", False)),
                       True)
    await check_next_instruction(match)


async def generate_matches(state: MatchState):
    for pick in state.picks:
        state.matches.append((pick, None))
    # TODO : handle more than 2 matches

    await state.main_channel.send(
        generate_announcement_message(state.players, state.bans,
                                      state.matches))


def generate_ban_message(player: discord.Member, opponent: discord.Member,
                         bans: list[str | None]):
    msg = f"""
    Bonjour <@{player.id}>. Afin de planifier ton match contre {opponent.display_name},
    nous avons besoin que tu bannisses l'une des catégories. Si tu ne souhaites
    bannir aucune catégorie, c'est bien évidemment ton droit."""
    if len(bans) > 0:
        msg += f"""\n{"Ton adversaire n'a banni aucune catégorie" if bans[-1] is None else f"Ton adversaire a banni la catégorie suivante : {bans[-1]}"}"""
    return msg


def generate_pick_message(player: discord.Member, opponent: discord.Member,
                          picks: list['str']):
    last_pick = None if len(picks) == 0 else picks[-1]

    return f"""
    Bonjour <@{player.id}>, les bans ayant été effectués, il est maintenant temps de choisir un mode.
    {f"Ton adversaire a choisi le mode suivant: {last_pick}" if last_pick else ""}
    """


def generate_announcement_message(players: tuple[discord.Member,
                                                 discord.Member],
                                  bans: list[str | None],
                                  matches: list[tuple[str,
                                                      discord.Member | None]]):
    return f"""
    Merci <@{players[0].id}> et <@{players[1].id}>. Vous avez achevé vos corvées administratives et vous pouvez maintenant jouer :)

    **Le(s) catégorie(s) suivante(s) ont été bannie(s) :** {', '.join([mode for mode in bans if mode is not None])}
    **Les modes suivants ont été choisis:** {', '.join([match[0] for match in matches])}
    """
