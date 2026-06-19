""" read the function :3
"""
import discord


def get_channel_by_id(guild: discord.Guild, channel_id: int):
    """get a server category from its id

    Args:
        guild (discord.Guild): the server
        category_id (int): the id

    Returns:
        discord.CategoryChannel: the category
    """
    return discord.utils.get(guild.channels, id=channel_id)
