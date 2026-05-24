""" read the function :3
"""
import discord


async def get_or_create_role(guild: discord.Guild, role_name: str):
    """get a role from a server by its name. Create it first if it's not found

    Args:
        guild (discord.Guild): the server
        role_name (str): the name

    Returns:
        discord.Role: the role
    """
    role = discord.utils.get(guild.roles, name=role_name)

    if role is None:
        role = await guild.create_role(name=role_name)

    return role
