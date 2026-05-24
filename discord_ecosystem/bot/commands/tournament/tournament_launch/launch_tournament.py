import json
import discord.ui
import time
import discord
from random import shuffle
from common.actions.get_category_from_server_by_id import get_category_by_id
from common.actions.create_channel import create_restricted_text_channel
from common.actions.get_or_create_role import get_or_create_role
from common.actions.assign_roles_to_users import assign_roles_to_users
from common.actions.get_user import get_member_by_id
from common.actions.send_message import send_message
from bot.commands.tournament.tournament_launch.utils.pick_ban import start_pick_ban

from bot.ui.confirm_view import SimpleConfirmView
from common.bot_state import Tournament


class channelLinksView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(label="Règlement du Tournoi",
                              url="https://perdu.com"))
        self.add_item(
            discord.ui.Button(label="Liste des modes et presets",
                              url="https://perdu.com"))
        self.add_item(
            discord.ui.Button(label="Formulaire d'inscription",
                              url="https://perdu.com"))


class threadLinksView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(label="Voir les catégories",
                              url="https://perdu.com"))
        self.add_item(
            discord.ui.Button(
                label="Un bon restaurant pour un steak de cheval",
                url="https://perdu.com"))


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
    msg = f"""Bonjour, <@{users[0].id}> et <@{users[1].id}>. J'espère que vous allez bien
    et que vous êtes prêts à passer un bon moment pendant ce tournoi. Lors de cette phase de
    groupe, vous aurez le droit chacun de bannir une catégorie, ce qui n'est pas obligatoire. \n
    {users[0].name}, tu as été tiré au hasard pour bannir une catégorie en premier.
    Une fois que tu l'auras fait, {users[1].name} pourra bannir une catégorie également. \n
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


async def create_tournament_structure(interaction: discord.Interaction,
                                      json_config: discord.Attachment):
    """ This function should create a tournament structure from a JSON. The JSON is formatted as such:
        {
            "category_name": "the name of the category under which it should create a structure"
            "groups" [
                "role_name":"string",
                "players": ["player 1, "player 2"]
            ]
        }

        this will

        in the category :
            create one text channel, reserved to `role_name` and `admins`
            ping the role with a given message that will give them the instructions needed for the tournament (players length dependent)
            send the message to the channel
            make player pairs
            for each player pair (3 players : 3 pairs --> 3 matches per pair, 4 players: 6 pairs) --> 2 matches per pair
                create a private thread
                invite both player
                give them a message on how to ban
                select one at random for the first ban, they will also get first pick

        Args:
            config_json (_type_): _description_
        """
    if not interaction.guild:
        await interaction.response.send_message(
            "Cette commande ne peut être lancée que depuis un serveur")
        return
    await interaction.response.send_message(
        "Merci d'avoir lancé la commande de création de tournoi, nous allons vérifier que tout soit en ordre"
    )
    guild = interaction.guild
    data = await validate_and_return_json_config(json_config, interaction,
                                                 guild)
    if not data:
        await interaction.followup.send("Annulation de la création du tournoi",
                                        ephemeral=True)
        return
    if Tournament.is_tournament_ongoing():
        await interaction.followup.send(
            "Une phase de groupe a déjà été lancée, désolé")
        return
    await ask_to_check_config(interaction, guild, data)


async def ask_to_check_config(interaction: discord.Interaction,
                              guild: discord.Guild, data: dict):
    view = SimpleConfirmView(generate_structure, guild=guild, data=data)

    msg = "Merci de vérifier que les groupes soient corrects :3 \n"
    msg += '\n'.join(
        [group_to_string(group, guild) for group in data["groups"]])
    await interaction.followup.send(msg, view=view)


def group_to_string(group: dict, guild: discord.Guild):
    members_name: list[str] = [
        get_member_by_id(guild, id).name for id in group["players"]
    ]
    return f"**{group['role_name']}** : {', '.join(members_name)}"


async def generate_structure(interaction: discord.Interaction, options: dict):

    if not options.get("guild") or not options.get("data"):
        await interaction.response.send_message(
            "je sais pas pourquoi, mais ça a merdé")
        return
    if Tournament.is_tournament_ongoing():
        await interaction.response.send_message(
            "Un tournoi est déjà en cours. Je suppose que vous avez appuyé plusieurs fois sur 'confirmer', petit.e malandrin.e"
        )
        return
    guild = options["guild"]
    data = options["data"]
    Tournament.set_tournament_state({"groups": data["groups"]})

    await interaction.response.send_message(
        "Merci d'avoir confirmé, nous continuons le processus")
    category: discord.CategoryChannel = get_category_by_id(
        guild, data["category_id"])

    groups: list = data["groups"]

    general_role: discord.Role = await get_or_create_role(
        guild, data["general_role_name"])

    for group in groups:

        role_name: str = group["role_name"]
        players_ids: list[int] = group["players"]
        channel_name = f"""organisation-groupe-{role_name}"""
        group_role: discord.Role = await get_or_create_role(guild, role_name)
        roles = [group_role, general_role]
        users: list[discord.Member] = [
            get_member_by_id(guild, user_id) for user_id in players_ids
        ]
        await assign_roles_to_users(roles, users)
        channel: discord.TextChannel = await create_restricted_text_channel(
            guild, category, channel_name, [group_role])
        time.sleep(2)
        channel_msg: str = create_channel_msg(group_role, len(users))
        await send_message(recipient=channel,
                           message=channel_msg,
                           view=channelLinksView())
        player_pairs: list[list[discord.Member]] = create_player_pairs(users)
        await interaction.followup.send(
            "Nous lançons la phase de pick et de bans :3")
        for pair in player_pairs:
            await start_pick_ban(pair[0], pair[1], channel)
            #thread = await create_restricted_thread(
            #    channel, pair,
            #    f"""Organisation - {pair[0].name} vs. {pair[1].name}""")
            #time.sleep(2)
            #thread_msg = create_thread_msg(pair, len(users))
            #await send_message(thread, thread_msg, None)


async def validate_and_return_json_config(json_file: discord.Attachment,
                                          interaction: discord.Interaction,
                                          guild: discord.Guild):
    is_falsy = False
    try:
        data = json.loads(await json_file.read())
        if not isinstance(data, dict):
            await interaction.followup.send("Le JSON reçu n'est pas un objet",
                                            ephemeral=True)
            return None
        if not isinstance(data.get("category_id", None),
                          int) or not get_category_by_id(
                              guild, data["category_id"]):
            await interaction.followup.send(
                "category_id doit être présente et doit être une ID de catégorie présente sur le serveur",
                ephemeral=True)
            is_falsy = True
        if not isinstance(data.get("general_role_name", None), str):
            await interaction.followup.send(
                "general role name doit être une chaîne de caractère",
                ephemeral=True)
            is_falsy = True
        if not isinstance(data.get("groups", None), list) or len(
                data["groups"]) == 0:
            await interaction.followup.send(
                "Il doit y avoir un champ 'groups' qui contient au moins un objet",
                ephemeral=True)
            is_falsy = True
        else:
            for group in data["groups"]:
                if not (isinstance(group, dict)):
                    is_falsy = True
                    await interaction.followup.send(
                        "Chaque groupe doit être un objet", ephemeral=True)
                else:
                    if not isinstance(group.get("role_name", None), str):
                        await interaction.followup.send(
                            "Le champ 'role_name' doit être présent dans un groupe et être une chaîne de caractères",
                            ephemeral=True)
                        is_falsy = True
                    if not isinstance(group.get("players", None), list):
                        await interaction.followup.send(
                            "Le champ 'players' doit être une liste d'entiers représentants les ID des joueurs",
                            ephemeral=True)
                        is_falsy = True
                    elif len([
                            playerid for playerid in group["players"]
                            if isinstance(playerid, int)
                    ]) < len(group["players"]):
                        is_falsy = True
                        await interaction.followup.send(
                            "Tous les ids d'un des groupes ne sont pas des entiers",
                            ephemeral=True)

        return data if not is_falsy else None

    except Exception as e:
        print(e)
        await interaction.followup.send(
            "Une erreur s'est produite pendant la lecture du fichier de configuration. Dommage hein ?",
            ephemeral=True)
