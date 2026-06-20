import json
import requests
import discord
from discord import app_commands
from common.relevant_channels import RelevantChannels


@app_commands.command(name="resultat")
async def send_result(interaction: discord.Interaction, racetime_id: str):
    if not interaction.guild:
        await interaction.response.send_message(
            "Cette commande ne peut être lancée que depuis un serveur :3")
        return
    channel: discord.TextChannel | None = RelevantChannels.getSpecificChannel(
        interaction.guild, "dashboard")
    if not channel:
        await interaction.response.send_message(
            "Le canal pour donner les résultats n'a pas été défini. Merci de contacter les admins pour leur signaler.",
            ephemeral=True)
        return

    await interaction.response.send_message(
        "Nous allons transferrer le résultat, merci beaucoup.")

    entrants_data = await get_result(interaction, racetime_id)
    if entrants_data is None:
        return
    message = ""
    if len(entrants_data) > 2:
        message = "\n".join([
            f"Résultat pour la race room https://racetime.gg/alttpr/{racetime_id}",
            *[format_result(entrant) for entrant in entrants_data]
        ])
    else:
        message = format_short_result(entrants_data, racetime_id)
    await channel.send(message, silent=True)


async def get_result(interaction, racetime_id):
    raceroom_query = requests.get(
        f"https://racetime.gg/alttpr/{racetime_id}/data")
    if raceroom_query.status_code != 200:
        await interaction.followup.send(
            "Nous n'avons pas pu nous connecter à la room.", ephemeral=True)
        return None
    data = json.loads(raceroom_query.content)
    if data["status"]["value"] != "finished":
        await interaction.followup.send("La course n'est pas terminée",
                                        ephemeral=True)
        return None
    return data["entrants"]


def format_result(user_object: dict):
    full_name = user_object["user"]["full_name"]
    place = user_object["place"]
    finish_time = user_object["finish_time"]
    if place is None:
        return f"""
    {full_name} n'a pas terminé la course"""
    return f"""
    {full_name} a terminé la course en {place}{"ère" if place == 1 else "ème"} position avec un temps de {format_time(finish_time)}.
    """


def format_short_result(entrants, rt_id):
    names = [entrant["user"]["name"] for entrant in entrants]
    full_names = [entrant["user"]["full_name"] for entrant in entrants]
    times = [format_time(entrant["finish_time"], True) for entrant in entrants]
    return f"**Match {names[0]} vs {names[1]}: ** | {full_names[0]} : {times[0]} | {full_names[1]} : {times[1]} | raceroom: https://racetime.gg/alttpr/{rt_id}"


def format_time(timestr: str, short=False):
    if not timestr:
        return 'DNF'
    first_split = timestr.replace("P0DT", "").split("H")
    full_split = [first_split[0], *first_split[1].split("M")]
    full_split[2] = full_split[2][0:5]
    for i in range(len(full_split)):
        if (full_split[i].startswith('0')):
            full_split[i] = full_split[i].replace("0", "", 1)
    if short:
        return ':'.join(full_split)
    return f"{full_split[0]} Heure{'s' if int(full_split[0]) > 1 else ''}, {full_split[1]} Minute{'s' if int(full_split[1]) > 1 else ''} et {full_split[2]} Seconde{'s' if float(full_split[2]) > 1 else ''}"
