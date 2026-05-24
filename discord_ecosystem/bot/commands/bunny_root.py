from discord import app_commands
from bot.commands.tournament.tournament_group import tournament
from bot.commands.base.help_command import send_help
from bot.commands.sudo.sudo_group import sudo


class Bunny(app_commands.Group):

    def __init__(self, name):
        super().__init__(name=name, description="Main bot commands")
        self.add_command(tournament)
        self.add_command(sudo)
        self.add_command(send_help)
