import discord
from discord import app_commands
from bot.commands.tournament.launch.initialize import initialize
from bot.utils.permissions import requires_group

tournament = app_commands.Group(
    name="tournament", description="Commandes utilisées pour les tournois")


@tournament.command(name="initialize")
@requires_group(group="tournament")
@app_commands.guild_only()
async def initialize_tournament(interaction: discord.Interaction,
                                json_config: discord.Attachment):
    if not interaction.guild:
        await interaction.response.send_message(
            "This command is only usable within a guild context")
        return
    await initialize(interaction, interaction.guild, json_config)


@tournament.command(name="continue")
@requires_group(group="tournament")
@app_commands.guild_only()
async def continue_tournament(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(
            "This command is only usable within a guild context")
        return
    print(
        "here, we would need to restart the tournament from the current state")
