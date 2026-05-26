import discord

from bot.commands.tournament.launch.steps.can_we_start import can_we_start_tournament
from bot.commands.tournament.launch.steps.confirm_config import confirm_config

from common.bot_state import TournamentsStates, TournamentStatesEnum


async def initialize(interaction: discord.Interaction, guild: discord.Guild,
                     json_config: discord.Attachment):
    if TournamentsStates.get_status(
            guild.id) != TournamentStatesEnum.INITIAL_STATE:
        await interaction.response.send_message("""
    Bonjour, un tournoi est déjà en cours sur ce serveur :3
    """)

    await interaction.response.send_message("""
    Bonjour et merci d'essayer de lancer un tournoi. Nous allons vérifier que tout soit en ordre.
    """)
    TournamentsStates.update_status(guild.id, TournamentStatesEnum.VALIDATING)
    data = await can_we_start_tournament(interaction, guild, json_config)
    if not data:
        TournamentsStates.update_status(guild.id, TournamentStatesEnum.ERROR)
        return
    await confirm_config(interaction, guild, data)
