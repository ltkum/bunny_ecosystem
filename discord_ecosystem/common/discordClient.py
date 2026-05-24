"""
    Singleton Client for the application

"""
import os
import discord
from discord.ext import commands
from bot.commands.bunny_root import Bunny


class DiscordClient():
    """ Guess what I said before

    Raises:
        Exception: without authentication, it should fail :3

    Returns:
        discord.Bot: yes, a bot
    """
    bot = None

    @classmethod
    def get_client(cls):
        if not cls.bot:
            intents = discord.Intents.default()
            intents.guilds = True
            intents.members = True

            cls.bot = commands.Bot(command_prefix="!", intents=intents)
            bunny = Bunny()
            cls.bot.tree.add_command(bunny)

        return cls.bot

    @classmethod
    def run(cls):
        discord_token = os.getenv('DISCORD_BOT_AUTH_TOKEN', None)
        if not discord_token:
            raise Exception('No discord token given')

        cls.get_client().run(discord_token)

    @classmethod
    def get_guild(cls, guild_id):
        return cls.get_client().get_guild(guild_id)
