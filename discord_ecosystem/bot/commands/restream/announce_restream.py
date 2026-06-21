import time
import json
import requests
import discord

rt_gg_id_to_disc_id = {
    "Metroid_04#2479": 235172798446698500,
    "retro_redfield#3039": 157144653580337152,
    "falcon#0815": 325480657134288907,
    "fellys#6132": 278676262883557376,
    "Gridasham#3379": 386981995504336898,
    "thePa1ne#8901": 576580561133371395,
    "Zorimyll#7692": 110086041083326464,
    "Reynox#6303": 259540285380362242,
    "Phyrie#5520": 254933538892283905,
    "kefffka#6024": 350577143081730048,
    "Baku#3629": 250671836763783170,
    "Paraducks64#0459": 141700342277603328,
    "Akaelyne#9090": 278174613672951808,
    "Scaryolive#5959": 184828592499326977,
    "LittleMsArcade#1793": 397471450359005184,
    "Kan7os#8890": 156125658559414272,
    "Derthys#6130": 138698063316385792,
    "Shyniste#4854": 455265379082567681,
    "Beth#1108": 213124945587339267,
    "Rywek#6652": 194887170161508352,
    "Yukikaze#5523": 121032824907104262,
}


async def announce_restream(interaction: discord.Interaction,
                            player_1: discord.Member, player_2: discord.Member,
                            channel: discord.TextChannel, when_in_minutes: int,
                            mode: str, is_there_a_restream: bool,
                            racetime_room_id: str):
    racetime_data = requests.get(
        f"https://racetime.gg/alttpr/{racetime_room_id}/data", timeout=10)
    if racetime_data.status_code != 200:
        await interaction.followup.send(
            "Une erreur s'est produite et nous n'avons pas pu récupérer les données racetimes."
        )
    players: dict[discord.Member, str] = racetime_data_to_player_data(
        interaction.guild, json.loads(racetime_data.content))

    await player_1.send(
        format_player_message(player_1, player_2, racetime_room_id,
                              is_there_a_restream))
    await player_2.send(
        format_player_message(player_2, player_1, racetime_room_id,
                              is_there_a_restream))
    await channel.send(
        format_channel_message(when_in_minutes, is_there_a_restream, player_1,
                               player_2, players, mode))


def format_player_message(player: discord.Member, opponent: discord.Member,
                          racetime_room_id: str, official_restream: bool):
    return f"""
    Bonjour {player.display_name}. Tu as un match très prochainement contre {opponent.display_name}.
    {"Ce match aura un restream. Un membre de l'équipe de restream s}era présent dans la race room pour discuter avec vous deux et prendre les informations nécessaires." if official_restream else ""}
    Tu peux déjà rejoindre la race room ici : https://racetime.gg/alttpr/{racetime_room_id}
    """


def format_channel_message(in_minutes: int, restream: bool,
                           player_1: discord.Member, player_2: discord.Member,
                           players_data: dict[discord.Member, str], mode: str):
    msg = f"""
    **Annonce de  Match **
    ** Qui joue?: ** {player_1.display_name} vs {player_2.display_name}
    ** Quand le match devrait-il commencer ? :** <t:{int(time.time()) + (in_minutes * 60)}:f>
    ** Quel Mode ? :** {mode}
    ** Où voir ça ? :** {"https://multistre.am/"+players_data.get(player_1, "")+"/"+players_data.get(player_2, "")+"/layout4/" if not restream else "https://www.twitch.tv/zeldaspeedrunsfr"}

    N'hésitez pas à aller encourager les participant.es, et bonne chance à ces dernier.ères !
    """

    return msg


def rtid_to_disc_member(guild: discord.Guild, rt_gg_id: str):

    return guild.get_member(rt_gg_id_to_disc_id[rt_gg_id])


def racetime_data_to_player_data(guild: discord.Guild, racetime_data):

    players_data: dict[discord.Member, str] = {}
    for user in racetime_data["entrants"]:
        players_data[rtid_to_disc_member(
            guild, user["user"]["full_name"])] = user["user"]["twitch_name"]
    return players_data
