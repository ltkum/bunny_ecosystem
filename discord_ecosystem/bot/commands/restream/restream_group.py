from discord import app_commands
import discord
from bot.utils.permissions import requires_group

from common.relevant_channels import RelevantChannels
from bot.commands.restream.ask_for_crew import ask_for_crew
from bot.commands.restream.ask_for_broadcast_operator import ask_for_bo
from bot.commands.restream.announce_restream import announce_restream

restream = app_commands.Group(
    name="restream",
    description=
    "Commandes utilisées pour les fonctions de gestion des restreams vis à vis du bot"
)


@restream.command(name="look_for_bo")
@requires_group(group="restream")
@app_commands.guild_only()
async def look_for_restream_bos(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(
            "This interaction is only usable in a guild")
        return
    channel = RelevantChannels.getSpecificChannel(interaction.guild,
                                                  "bo_channel")
    if not channel:
        await interaction.response.send_message(
            "Le canal des broadcasts operators n'a pas été configuré sur ce serveur :3"
        )
        return
    await ask_for_bo(interaction, channel)


@restream.command(name="look_for_crew")
@requires_group(group="restream")
@app_commands.guild_only()
async def look_for_restream_crew(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(
            "This interaction is only usable in a guild")
        return
    channel = RelevantChannels.getSpecificChannel(interaction.guild,
                                                  "crew_channel")
    if not channel:
        await interaction.response.send_message(
            "Le canal des équipes de restreams n'a pas été configuré sur ce serveur :3"
        )
        return
    await ask_for_crew(interaction, channel)
    pass


@restream.command(name="annoncer_match")
@requires_group(group="restream")
@app_commands.guild_only()
async def announce_match(interaction: discord.Interaction,
                         joueur_1: discord.Member, joueur_2: discord.Member,
                         canal_annonce: discord.TextChannel,
                         dans_combien_de_minutes_en_gros: int, mode: str,
                         on_a_une_équipe_de_restream: bool,
                         racetime_room_id: str):
    if not interaction.guild:
        await interaction.response.send_message(
            "Cette fonction ne marche pas hors d'un serveur :3")
    await interaction.response.send_message(
        "Nous allons essayer d'annoncer le match, merci de patienter quelques secondes :3"
    )
    await announce_restream(interaction, joueur_1, joueur_2, canal_annonce,
                            dans_combien_de_minutes_en_gros, mode,
                            on_a_une_équipe_de_restream, racetime_room_id)
