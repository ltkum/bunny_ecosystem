from dis import disco
import requests
import os
from aiohttp.web import view
import discord
from bot.ui.views.link_buttons_view import LinksButtonView
from common.relevant_roles import RelevantRoles


def format_crew_search_msg(matches_array: list, guild: discord.Guild):
    msg = f"""
    Bonjour à tous chers <@&{RelevantRoles.getRoleFromGuild(guild, 'tracker')}> et <@&{RelevantRoles.getRoleFromGuild(guild, 'commentator')}>. J'espère que vous allez bien.
    Les matchs suivants vont avoir lieu d'ici à 7 jours et cherchent encore des volontaires pour permettre un restream.
    """
    for match in matches_array:
        if match.get(
                "event", ""
        ) == "ALttPR Tournoi francophone 9e Édition" and match_needs_crew(
                match):
            msg += format_single_match(match)
    return msg


def match_needs_crew(match):
    return match.get("allowed_restream", False) and match.get(
        "broadcast_operator", None) and len(
            match.get("commentators", "").split(',')) < 2 and len(
                match.get("trackers", "").split(',')) < 2


def format_single_match(match):
    comm_needed = 2 - len(match["commentators"].split(','))
    if match["commentators"] == "":
        comm_needed += 1
    comm_needed_msg = f"{str(comm_needed) + ' commentateur' if comm_needed > 0 else ''}{'s' if comm_needed > 1 else ''}"
    track_needed = 2 - len(match["trackers"].split(','))
    if match["trackers"] == "":
        track_needed += 1
    track_needed_msg = f"{' et' if comm_needed > 0 and track_needed > 0 else ''}{' ' + str(track_needed) + ' traqueur' if track_needed > 0 else ''}{'s' if track_needed>1 else ''}"
    ronde = match["round"]
    mode = match["mode"]
    return f"""
<t:{match["timestamp"]}:f> : {ronde} - **{match["matchup"]}** {' - ' + mode if mode is not None else ''}.
Il nous manque encore {comm_needed_msg}{track_needed_msg}."""


async def ask_for_crew(interaction: discord.Interaction,
                       channel: discord.TextChannel):
    await interaction.response.send_message(
        "Merci, nous allons récupérer les informations, puis envoyer les messages. Celà peut prendre quelques secondes."
    )
    query = requests.get(os.getenv("GOOGLE_SCRIPT_SCHEDULE_LINK", ""),
                         timeout=10)
    if query.status_code != 200:
        await interaction.followup.send(
            "Une erreur a eu lieu, merci de patienter quelques minutes puis réessayer. Si l'erreur persiste, dommage :3"
        )
        return
    await channel.send(content=format_crew_search_msg(query.json(),
                                                      interaction.guild),
                       silent=True,
                       view=LinksButtonView([
                           ("Se porter volontaire",
                            os.getenv("ZSFR_SIGNUP_SHEET",
                                      'https://perdu.com'))
                       ]))
    # here we fetch the JSON
    # we create the message
    # we send it to the relevant channel
