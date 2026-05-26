""" Not hard to understand
"""
import discord


async def send_message(recipient: discord.Member | discord.TextChannel
                       | discord.Thread
                       | discord.User,
                       message: str,
                       view: discord.ui.View | None,
                       silent: bool = False):
    """Send a message

    Args:
        recipient (discord.Member | discord.TextChannel | discord.Thread | discord.User): Who receives
        message (str): what to send
        view (discord.ui.View | None): UI elements
    """
    if view:
        await recipient.send(message, view=view, silent=silent)
    else:
        await recipient.send(message, silent=silent)
