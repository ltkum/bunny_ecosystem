from unicodedata import category
import discord
from bot.ui.views.confirm_view import SimpleConfirmView


class PickCategorySelect(discord.ui.Select):

    def __init__(self, parent_view, state):

        options = [
            discord.SelectOption(label=category)
            for category in parent_view.data.keys()
        ]

        super().__init__(placeholder="Choisissez une catégorie",
                         min_values=1,
                         max_values=1,
                         options=options)

        self.parent_view = parent_view
        self.state = state

    async def callback(self, interaction: discord.Interaction):

        selected_category = self.values[0]

        self.parent_view.selected_category = selected_category

        # Update item select
        self.parent_view.update_item_select()

        await interaction.response.edit_message(view=self.parent_view)


class PickModeSelect(discord.ui.Select):

    def __init__(self, parent_view, items, callback_fn):

        options = [discord.SelectOption(label=item) for item in items]

        super().__init__(placeholder="Choisissez un Mode",
                         min_values=1,
                         max_values=1,
                         options=options)

        self.parent_view = parent_view
        self.callback_fn = callback_fn

    async def callback(self, interaction: discord.Interaction):

        self.parent_view.selected_item = self.values[0]
        confirm_view = SimpleConfirmView(
            confirm_callback=self.callback_fn,
            category=self.parent_view.selected_category,
            mode=self.parent_view.selected_item,
            state=self.parent_view.state)

        await interaction.response.send_message(
            f"Vous avez choisi: **{self.parent_view.selected_item}**\n",
            view=confirm_view,
            ephemeral=True)


class PickView(discord.ui.View):

    def __init__(self, data, state, callback_fn):

        super().__init__(timeout=300)

        self.data = data

        self.selected_category = None
        self.selected_item = None
        self.item_select = None
        self.callback_fn = callback_fn
        self.state = state
        self.category_select = PickCategorySelect(self, state)

        self.add_item(self.category_select)

    def update_item_select(self):

        # Remove old item select
        for item in self.children[:]:
            if isinstance(item, PickModeSelect):
                self.remove_item(item)

        # Add new item select
        items = self.data[self.selected_category].get("modes", [])

        self.item_select = PickModeSelect(self, items, self.callback_fn)

        self.add_item(self.item_select)
