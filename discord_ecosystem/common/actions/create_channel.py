""" read the function :3
"""
import discord


async def create_text_channel(guild: discord.Guild,
                              category: discord.CategoryChannel,
                              channel_name: str, **kwargs):
    """Generic function to create a text channel.

    Args:
        guild (discord.Guild): The server in which to create the channel
        category (discord.CategoryChannel): The category on said server
        channel_name (str): The name of the channel

        supported keywords args:
            - restricted: boolean telling us if the channel should be restricted or open
            - allowed_roles: a list of roles which have the right to read / write on said channel

    Returns:
        discord.TextChannel: the channel we just created.
    """
    overwrites: dict[discord.Role | discord.Member | discord.Object,
                     discord.PermissionOverwrite] = {
                         guild.default_role:
                         discord.PermissionOverwrite(read_messages=True,
                                                     send_messages=True),
                         guild.me:
                         discord.PermissionOverwrite(read_messages=True,
                                                     send_messages=True)
                     }

    if kwargs.get("restricted", False):
        overwrites[guild.default_role] = discord.PermissionOverwrite(
            read_messages=False,
            send_messages=False)  # we create a restricted channel
        for role in kwargs.get("allowed_roles", []):
            overwrites[role] = discord.PermissionOverwrite(read_messages=True,
                                                           send_messages=True)
    channel = await guild.create_text_channel(channel_name,
                                              category=category,
                                              overwrites=overwrites)
    return channel


async def create_restricted_text_channel(guild: discord.Guild,
                                         category: discord.CategoryChannel,
                                         channel_name: str,
                                         allowed_roles: list[discord.Role]):
    overwrites: dict[discord.Role | discord.Member | discord.Object,
                     discord.PermissionOverwrite] = {
                         guild.default_role:
                         discord.PermissionOverwrite(read_messages=False),
                         guild.me:
                         discord.PermissionOverwrite(read_messages=True,
                                                     send_messages=True)
                     }

    for role in allowed_roles:
        overwrites[role] = discord.PermissionOverwrite(read_messages=True,
                                                       send_messages=True)
    channel = await guild.create_text_channel(channel_name,
                                              category=category,
                                              overwrites=overwrites)
    return channel
