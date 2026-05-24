""" read the function :3
"""
import discord


async def create_thread(channel: discord.TextChannel, thread_name: str,
                        private: bool, **kwargs):
    """Create a thread. If there are users or roles to invite, will do so

    Args:
        channel (discord.TextChannel): the channel in which we create the thread
        thread_name (str): name of the thread
        private (bool): tells if the thread is private or not
    Supported Keyword Args:
        users (list[discord.Member]): a list of user to invite to the thread
        roles (list[discord.Role]):  a list of roles to invite to the thread


    Returns:
        discord.Thread: the created thread
    """

    thread_type = discord.ChannelType.private_thread if private else discord.ChannelType.public_thread
    thread = await channel.create_thread(name=thread_name, type=thread_type)

    for user in kwargs.get("users", []):
        await thread.add_user(user)
    return thread


async def create_restricted_thread(channel: discord.TextChannel,
                                   users: list[discord.Member],
                                   thread_name: str):
    """Create a thread and add

    Args:
        channel (discord.TextChannel): _description_
        users (list[discord.Member]): _description_
        thread_name (str): _description_

    Returns:
        _type_: _description_
    """
    thread = await channel.create_thread(
        name=thread_name, type=discord.ChannelType.private_thread)

    for user in users:
        await thread.add_user(user)

    return thread
