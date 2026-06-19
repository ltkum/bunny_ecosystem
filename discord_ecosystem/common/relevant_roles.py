import discord


class RelevantRoles:

    guild_roles = None

    @classmethod
    def getGuilds(cls):
        if not cls.guild_roles:
            cls.guild_roles = {}
        return cls.guild_roles

    # this is always set wit hsetSpecificChannel
    @classmethod
    def setGuild(cls, guild):
        cls.getGuilds()[guild] = {}

    @classmethod
    def getRoleFromGuild(cls, guild: discord.Guild, role_function: str):
        return cls.getGuilds().get(guild, {}).get(role_function, None)

    @classmethod
    def setRoleFromGuild(cls, guild: discord.Guild, role_function: str,
                         role_id: int):
        if not cls.getGuilds().get(guild, None):
            cls.setGuild(guild)
        cls.guild_roles[guild][role_function] = role_id
