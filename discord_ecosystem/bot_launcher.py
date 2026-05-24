"""
    Launcher for the application. This is what is called when we start the bot
"""
import discord
from common.discordClient import DiscordClient

BOT = DiscordClient.get_client()

GUILD_ID = 1501337781799092224  # test server id

guild = discord.Object(id=GUILD_ID)


@BOT.event
async def on_ready():
    """When the bot is read, it runs those commands.
        For now: it simply sync the commands and send them to the users so they can use them.
    """

    BOT.tree.copy_global_to(guild=guild)

    await BOT.tree.sync(guild=guild)
    print("Commands synced with test servers")

    await BOT.tree.sync()
    print("Commands Synced globally")


if __name__ == "__main__":
    DiscordClient.run()
