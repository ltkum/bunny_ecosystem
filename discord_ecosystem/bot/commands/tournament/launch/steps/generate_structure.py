import discord
import time

from random import shuffle

from common.actions.get_category_from_server_by_id import get_category_by_id
from common.actions.get_or_create_role import get_or_create_role
from common.actions.get_user import get_member_by_id
from common.actions.create_channel import create_text_channel
from common.actions.assign_roles_to_users import assign_roles_to_users
from common.actions.send_message import send_message
from common.actions.create_thread import create_thread
from common.bot_state import TournamentsStates, TournamentStatesEnum

from bot.commands.tournament.launch.utils.pick_ban import pick_ban_process
from bot.ui.views.link_buttons_view import LinksButtonView
from bot.ui.views.callback_buttons_view import CallbackButtonView, ButtonDefinition

channelLinks = [("Formulaire d'inscription", "https://perdu.com"),
                ("Règlement du tournoi", "https://perdu.com"),
                ("Liste des modes", "https://perdu.com")]


async def generate_structure(interaction: discord.Interaction,
                             guild: discord.Guild, data: dict):
    """
        generate the structure for the tournament and save it to the state,
        then starts the pick / ban phase of the tournament
    """

    if TournamentsStates.get_status(
            guild.id) != TournamentStatesEnum.VALIDATING:
        await interaction.response.send_message(
            "Un tournoi est déjà en cours. Je suppose que vous avez appuyé plusieurs fois sur 'confirmer', petit.e malandrin.e"
        )
        return
    TournamentsStates.update_status(guild.id,
                                    TournamentStatesEnum.CREATING_STRUCTURE)
    TournamentsStates.store_config(guild.id, data)

    await interaction.response.send_message(
        "Merci d'avoir confirmé, nous continuons le processus")
    category: discord.CategoryChannel = get_category_by_id(
        guild, data["category_id"])

    groups: list = data["groups"]

    general_role: discord.Role = await get_or_create_role(
        guild, data["general_role_name"])

    for group in groups:
        await manage_group(interaction, guild, category, general_role, group,
                           data["tournament_modes"])


async def manage_group(interaction: discord.Interaction, guild: discord.Guild,
                       category: discord.CategoryChannel,
                       general_role: discord.Role, group, categories):
    role_name: str = group["role_name"]
    players_ids: list[int] = group["players"]
    channel_name = f"""organisation-groupe-{role_name}"""
    group_role: discord.Role = await get_or_create_role(guild, role_name)
    roles = [group_role, general_role]
    users: list[discord.Member] = [
        get_member_by_id(guild, user_id) for user_id in players_ids
    ]
    await assign_roles_to_users(roles, users)
    channel: discord.TextChannel = await create_text_channel(
        guild,
        category,
        channel_name,
        restricted=True,
        allowed_roles=[group_role])
    time.sleep(2)
    channel_msg: str = create_channel_msg(group_role, len(users))
    # TODO here: get channel links from config
    await send_message(recipient=channel,
                       message=channel_msg,
                       view=LinksButtonView(channelLinks),
                       silent=True)
    player_pairs: list[list[discord.Member]] = create_player_pairs(users)
    await interaction.followup.send(
        "Nous créons les Threads pour les joueurs :3")
    for pair in player_pairs:
        thread: discord.Thread = await create_thread(
            channel=channel,
            thread_name=
            f"""Organisation - {pair[0].display_name} vs. {pair[1].display_name}""",
            private=True,
            users=pair)
        time.sleep(2)
        await send_message(recipient=thread,
                           message=create_thread_msg(
                               users=pair, nb_players_group=len(group)),
                           view=None,
                           silent=True)
        return
        # WE ARE NOT HANDLING THE PICK/BAN PHASE THROUGH
        button_definition = ButtonDefinition(
            "Lancez la phase de pick / ban", pick_ban_process, {
                "player1": pair[0],
                "player2": pair[1],
                "result_channel": channel,
                "thread": thread,
                "categories": categories,
                "third_match_needed": len(group) == 3,
                "message": "Merci beaucoup, nous allons lancer la phase de ban"
            }, discord.ButtonStyle.green)
        launch_ban_view = CallbackButtonView([button_definition])
        await send_message(thread,
                           create_thread_msg(pair, len(group)),
                           view=launch_ban_view,
                           silent=True)


def create_channel_msg(role, nb_players_group=4):
    return f"""Bonjour très chèr.es joueureuses du groupe <@&{role.id}> et
bienvenue dans nos phases de groupe. J'espère que vous passerez un agréable
tournoi en notre compagnie. \n\n
Cette phase de groupe durera du <t:1782079200:F> au <t:1785060000:F>. Durant cet intervalle,
vous aurez à effectuer {nb_players_group%2 + 2} matches contre chacun de vos adversaires.
Des fils vont être créés afin que chacun de vous puisse s'organiser avec les picks et bans.
Vous trouverez ci après quelques liens utiles.
"""


def create_thread_msg(users, nb_players_group=4):
    msg = f"""Bonjour, {users[0].display_name} et {users[1].display_name}. J'espère que vous allez bien
    et que vous êtes prêts à passer un bon moment pendant ce tournoi. Lors de cette phase de
    groupe, vous aurez le droit chacun de bannir une catégorie, ce qui n'est pas obligatoire. \n
    {users[0].display_name}, tu as été tiré au hasard pour bannir une catégorie en premier.
    Une fois que tu l'auras fait, {users[1].display_name} pourra bannir une catégorie également. \n
    Enfin, dans le même ordre, vous pourrez chacun choisir un mode. \n
    Nous vous rappelons que pendant les phases de groupe, une catégorie peut être choisie plusieurs fois."""

    if nb_players_group < 4:
        msg = f"""{msg}
    Comme vous devrez effectuer trois matches, pour le dernier match,
    vous devrez soit vous mettre d'accord sur un mode, soit tirer une roulette parmi tous
    les modes non bannis que vous n'avez pas joué. N'hésitez pas à demander à l'équipe de
    vous lancer une roulette :3"""
    return msg


def create_player_pairs(players):
    pairs: list[list[discord.Member]] = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            pairs.append([players[i], players[j]])

    # for pick ban: first in list will be first ban / pick
    for pair in pairs:
        shuffle(pair)

    return pairs
