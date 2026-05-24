""" read the function :3
    important distinction:
        User --> discord user
        Member --> member of a server
"""
import discord


def get_member_by_id(guild: discord.Guild, member_id: int):
    """ get a member from a server by its id

    Args:
        guild (discord.Guild): the server
        user_id (int): the id

    Returns:
        discord.Member | None: the member of nobody
    """
    return guild.get_member(member_id)
