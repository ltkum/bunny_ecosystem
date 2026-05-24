import discord
from discord import app_commands
from bot.commands.tournament.tournament_launch.launch_tournament import create_tournament_structure
from bot.utils.permissions import requires_group

tournament = app_commands.Group(
    name="tournament", description="Commandes utilisées pour les tournois")


@tournament.command(name="launch")
@requires_group(group="tournament")
async def launch_tournament(interaction: discord.Interaction,
                            json_config: discord.Attachment):
    await create_tournament_structure(interaction, json_config)
