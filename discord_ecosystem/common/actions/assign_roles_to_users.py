""" read the function :3
"""
import discord


async def assign_roles_to_users(roles: list[discord.Role],
                                users: list[discord.Member]):
    """ function assign roles to uses

    Args:
        roles (list[discord.Role]): a list of Roles to attribute
        users (list[discord.Member]): a list of Members which should receive the roles
    """
    for role in roles:
        for user in users:
            await user.add_roles(role)
