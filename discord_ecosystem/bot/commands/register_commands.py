from discord.ext.commands import Bot
from bot.commands.bunny_root import Bunny


# DEPRECTAED : to remove soon
def register_commands(bot: Bot):

    bunny = Bunny()
    bot.tree.add_command(bunny)
