""" read the function :3
"""
import discord


def get_category_by_id(guild: discord.Guild, category_id: int):
    """get a server category from its id

    Args:
        guild (discord.Guild): the server
        category_id (int): the id

    Returns:
        discord.CategoryChannel: the category
    """
    return discord.utils.get(guild.categories, id=category_id)
