from typing import final
import discord
from bot.ui.views.confirm_view import SimpleConfirmView


class Selector(discord.ui.Select):

    def __init__(self, choices, final_callback, placeholder, **kwargs):

        options = [discord.SelectOption(label=c) for c in choices]

        super().__init__(placeholder=placeholder,
                         min_values=1,
                         max_values=1,
                         options=options)

        self.final_callback = final_callback
        self.kwargs = kwargs

    async def callback(self, interaction: discord.Interaction):

        selected = self.values[0]

        confirm_view = SimpleConfirmView(self.final_callback,
                                         selected=selected,
                                         **self.kwargs)

        await interaction.response.send_message(
            f"Vous avez choisi: **{selected}**\n",
            view=confirm_view,
            ephemeral=True)


class SelectView(discord.ui.View):

    def __init__(self, choices, callback_fn, placeholder, **kwargs):

        super().__init__(timeout=300)

        self.add_item(Selector(choices, callback_fn, placeholder, **kwargs))
