import discord


class SimpleConfirmView(discord.ui.View):

    def __init__(self, confirm_callback, **kwargs):

        super().__init__(timeout=300)

        self.kwargs = kwargs
        self.confirm_callback = confirm_callback

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        await self.confirm_callback(interaction, **self.kwargs)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):

        await interaction.response.send_message("Sélection Annulée.",
                                                ephemeral=True)

        self.stop()
