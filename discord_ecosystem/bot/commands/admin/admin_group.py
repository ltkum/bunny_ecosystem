from discord import app_commands
import discord
from bot.utils.permissions import requires_group

from common.relevant_channels import RelevantChannels

admin = app_commands.Group(
    name="admin",
    description=
    "Commandes utilisées pour les fonctions d'administration vis à vis du bot")


@admin.command(name="set_dashboard_channel")
@requires_group(group="admin")
@app_commands.guild_only()
async def set_dashboard_channel(interaction: discord.Interaction,
                                text_channel: discord.TextChannel):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Cette fonctionalité ne fonctionne pas hors d'un serveur",
            ephemeral=True)
        return
    RelevantChannels.setSpecificChannel(interaction.guild, "dashboard",
                                        text_channel)
    await interaction.response.send_message(
        f"Le canal <#{text_channel.id}> est désormais notre canal de reporting. Merci de vous assurer que le bot a les droits requis"
    )


@admin.command(name="set_bo_channel")
@requires_group(group="admin")
@app_commands.guild_only()
async def set_bo_channel(interaction: discord.Interaction,
                         text_channel: discord.TextChannel):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Cette fonctionalité ne fonctionne pas hors d'un serveur",
            ephemeral=True)
        return
    RelevantChannels.setSpecificChannel(interaction.guild, "bo_channel",
                                        text_channel)
    await interaction.response.send_message(
        f"Le canal <#{text_channel.id}> est désormais notre canal de reporting. Merci de vous assurer que le bot a les droits requis"
    )


@admin.command(name="set_crew_channel")
@requires_group(group="admin")
@app_commands.guild_only()
async def set_crew_channel(interaction: discord.Interaction,
                           text_channel: discord.TextChannel):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Cette fonctionalité ne fonctionne pas hors d'un serveur",
            ephemeral=True)
        return
    RelevantChannels.setSpecificChannel(interaction.guild, "crew_channel",
                                        text_channel)
    await interaction.response.send_message(
        f"Le canal <#{text_channel.id}> est désormais notre canal de reporting. Merci de vous assurer que le bot a les droits requis"
    )
