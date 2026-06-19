import discord


class RelevantChannels:

    guild_channels = None

    @classmethod
    def getGuilds(cls):
        if not cls.guild_channels:
            cls.guild_channels = {}
        return cls.guild_channels

    @classmethod
    def setGuild(cls, guild):
        cls.guild_channels[guild] = {}

    @classmethod
    def getSpecificChannel(cls, guild: discord.Guild, channel_function: str):
        return cls.getGuilds().get(guild, {}).get(channel_function, None)

    @classmethod
    def setSpecificChannel(cls, guild: discord.Guild, channel_function: str,
                           channel: discord.TextChannel):
        if not cls.getGuilds().get(guild, None):
            cls.setGuild(guild)
        cls.guild_channels[guild][channel_function] = channel
