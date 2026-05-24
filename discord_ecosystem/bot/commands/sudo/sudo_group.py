import json
import discord
from discord import app_commands
from bot.utils.permissions import load_guild_config

sudo = app_commands.Group(
    name="sudo",
    description=
    "Commandes que seul les administrateurs du serveur peuvent utiliser")


@sudo.command(name="set_permissions")
async def set_permissions(interaction: discord.Interaction,
                          json_permission_config: discord.Attachment):
    if not interaction.guild_id or not isinstance(interaction.user,
                                                  discord.Member):
        return await interaction.response.send_message("Non")
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Admin only",
                                                       ephemeral=True)

    try:
        data = json.loads(await json_permission_config.read())

        load_guild_config(interaction.guild_id, data)
    except Exception:
        return await interaction.response.send_message(
            "Quelque chose s'est mal passé :3")
    await interaction.response.send_message("Permissions Mises à jour")
