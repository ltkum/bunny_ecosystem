from discord import app_commands
import discord
from bot.utils.permissions import requires_group
from bot.commands.weekly.launch_next_weekly_process import launch_next_weekly_process

weekly = app_commands.Group(
    name="weekly", description="Commandes utilisées pour aider les weeklys")


@weekly.command(name="launch")
@requires_group(group="weekly")
async def prepare_next_weekly(interaction: discord.Interaction,
                              json_config: discord.Attachment):
    await launch_next_weekly_process(interaction, json_config)
