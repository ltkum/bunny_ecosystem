"""
    Launcher for the application. This is what is called when we start the bot
"""
import os
from datetime import datetime
from common.discordClient import DiscordClient
from common.actions.get_channel_by_id import get_channel_by_id
from common.relevant_channels import RelevantChannels
from common.relevant_roles import RelevantRoles
import logging

logger = logging.getLogger("bunny")
BOT = DiscordClient.get_client()


async def assign_initial_channels_and_roles():
    for gd in ['TEST_SERVER', 'FFSFR_SERVER']:  # 'FFSFR_SERVER'

        guild = BOT.get_guild(int(os.getenv(f"{gd}_ID", "0")))
        if guild:

            initial_dashboard = get_channel_by_id(
                guild, int(os.getenv(f"{gd}_DASHBOARD_CHANNEL_ID", "0")))
            initial_bo_channel = get_channel_by_id(
                guild, int(os.getenv(f"{gd}_BO_CHANNEL_ID", default="0")))
            initial_crew_channel = get_channel_by_id(
                guild, int(os.getenv(f"{gd}_CREW_CHANNEL_ID", default="0")))
            if initial_dashboard:

                RelevantChannels.setSpecificChannel(guild, "dashboard",
                                                    initial_dashboard)
            if initial_bo_channel:
                RelevantChannels.setSpecificChannel(guild, "bo_channel",
                                                    initial_bo_channel)
            if initial_crew_channel:
                RelevantChannels.setSpecificChannel(guild, "crew_channel",
                                                    initial_crew_channel)
            RelevantRoles.setRoleFromGuild(
                guild, 'bo', int(os.getenv(f"{gd}_BO_ROLE_ID", "0")))
            RelevantRoles.setRoleFromGuild(
                guild, 'tracker', int(os.getenv(f"{gd}_TRACK_ROLE_ID", "0")))
            RelevantRoles.setRoleFromGuild(
                guild, 'commentator', int(os.getenv(f"{gd}_COMM_ROLE_ID",
                                                    "0")))


@BOT.event
async def on_ready():
    """When the bot is ready, it runs those commands.
        For now: it simply sync the commands and send them to the users so they can use them.
    """
    test_guild = BOT.get_guild(int(os.getenv("TEST_SERVER_ID", "0")))
    await assign_initial_channels_and_roles()

    if RelevantChannels.getSpecificChannel(test_guild, "dashboard"):
        await RelevantChannels.getSpecificChannel(
            test_guild, "dashboard"
        ).send(
            f"[<t:{datetime.now().timestamp().__floor__()}:s>] Je viens de démarrer ou de redémarrer."
        )
    BOT.tree.copy_global_to(guild=test_guild)

    await BOT.tree.sync(guild=test_guild)
    if RelevantChannels.getSpecificChannel(test_guild, "dashboard"):

        await RelevantChannels.getSpecificChannel(
            test_guild, "dashboard"
        ).send(
            f"[<t:{datetime.now().timestamp().__floor__()}:s>] Mes commandes sont maintenant utilisable sur le serveur de test."
        )

    await BOT.tree.sync()
    if RelevantChannels.getSpecificChannel(test_guild, "dashboard"):

        await RelevantChannels.getSpecificChannel(
            test_guild, "dashboard"
        ).send(
            f"[<t:{datetime.now().timestamp().__floor__()}:s>] Mes commandes sont maintenant utilisable sur tous les serveurs"
        )


if __name__ == "__main__":
    DiscordClient.run()
