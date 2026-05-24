import discord

NO_BAN = "Je ne souhaite pas bannir de mode"

categories = {
    "Open et Standard": {
        "bannable": False,
        "sur accord": False,
        "modes": ["open", "casual boots", "standard"]
    },
    "Keysanity | Clésordre": {
        "bannable": True,
        "sur accord": False,
        "modes": ["keysanity", "shopsanity"]
    },
    "Ennemizer": {
        "bannable": True,
        "sur accord": False,
        "modes": ["logical ennemizer", "logical bossmizer"]
    },
    "Inverted / Inversé": {
        "bannable": True,
        "sur accord": False,
        "modes": ["stanverted", "invrosia"]
    },
    "Entrances / Modes d'entrées": {
        "bannable": True,
        "sur accord": False,
        "modes": ["crosskeys", "retrance"]
    },
    "Modes Exotiques": {
        "bannable":
        False,
        "sur accord":
        True,
        "modes": [
            "spoiler", "HMG", "no logic double rod", "swordless", "doors",
            "MMMM"
        ]
    }
}


class BanSelect(discord.ui.Select):

    def __init__(self, choices, callback_fn):

        options = [discord.SelectOption(label=choice) for choice in choices]

        super().__init__(placeholder="Choisissez une catégorie à bannir",
                         min_values=1,
                         max_values=1,
                         options=options)

        self.callback_fn = callback_fn

    async def callback(self, interaction: discord.Interaction):

        selected = self.values[0]

        await self.callback_fn(interaction, selected)


class BanSelect2(discord.ui.Select):

    def __init__(self, choices, final_callback):

        options = [discord.SelectOption(label=c) for c in choices]

        super().__init__(placeholder="Choisissez une catégorie",
                         min_values=1,
                         max_values=1,
                         options=options)

        self.final_callback = final_callback

    async def callback(self, interaction: discord.Interaction):

        selected = self.values[0]

        confirm_view = ConfirmView(selected, self.final_callback)

        await interaction.response.send_message(
            f"Vous avez choisi: **{selected}**\n",
            view=confirm_view,
            ephemeral=True)


class ConfirmView(discord.ui.View):

    def __init__(self, selected_choice, confirm_callback):

        super().__init__(timeout=300)

        self.selected_choice = selected_choice
        self.confirm_callback = confirm_callback

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        await self.confirm_callback(interaction, self.selected_choice)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):

        await interaction.response.send_message("Sélection Annulée.",
                                                ephemeral=True)

        self.stop()


class PickCategorySelect(discord.ui.Select):

    def __init__(self, parent_view):

        options = [
            discord.SelectOption(label=category)
            for category in parent_view.data.keys()
        ]

        super().__init__(placeholder="Choisissez une catégorie",
                         min_values=1,
                         max_values=1,
                         options=options)

        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):

        category = self.values[0]

        self.parent_view.selected_category = category

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
        confirm_view = ConfirmView(self.parent_view.selected_item,
                                   self.callback_fn)
        await interaction.response.send_message(
            f"Vous avez choisi: **{self.parent_view.selected_item}**\n",
            view=confirm_view,
            ephemeral=True)


class PickView(discord.ui.View):

    def __init__(self, data, callback_fn):

        super().__init__(timeout=300)

        self.data = data

        self.selected_category = None
        self.selected_item = None
        self.item_select = None
        self.callback_fn = callback_fn
        self.category_select = PickCategorySelect(self)

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


class BanView(discord.ui.View):

    def __init__(self, choices, callback_fn):

        super().__init__(timeout=300)

        self.add_item(BanSelect2(choices, callback_fn))


async def start_pick_ban(player1: discord.Member, player2: discord.Member,
                         result_channel):

    state = {
        "remaining": [
            key for key in categories.keys()
            if categories[key].get("bannable", False)
        ],
        "player1_ban_choice":
        None,
        "player2_ban_choice":
        None,
        "player1_ban_choice_made":
        False,
        "player2_ban_choice_made":
        False,
        "player1_pick_choice":
        None,
        "player2_pick_choice":
        None,
        "player1_pick_choice_made":
        False,
        "player2_pick_choice_made":
        False,
    }

    # 1: we ask the first player to make a ban
    async def ask_first_ban():
        view = BanView(
            [
                *state["remaining"],  # ty:ignore[not-iterable]
                NO_BAN
            ],
            callback_first_ban)

        await player1.send(generate_ban_message(player2),
                           view=view,
                           silent=True)

    # 2: We receive the selection, we now ask for confirmation
    async def callback_first_ban(interaction: discord.Interaction, selected):
        if (state["player1_ban_choice_made"]):
            await interaction.response.send_message(
                f"Vous avez déjà effectué votre bannissement contre {player2.name}"
            )
            return
        else:
            await interaction.response.defer()
        state["player1_ban_choice"] = selected
        # SEND MESSAGE WITH BAN CONFIRM
        await callback_confirm_first_ban()

    # 3: we receive confirmation, we lock it in and we send the question to the second player
    async def callback_confirm_first_ban():
        state["player1_ban_choice_made"] = True
        await ask_second_ban()

    # 4: We ask the second player for the ban
    async def ask_second_ban():
        if (state["player1_ban_choice"] != NO_BAN):
            state["remaining"].remove(  # ty:ignore[unresolved-attribute]
                state["player1_ban_choice"]  # ty:ignore[invalid-argument-type]
            )
        view = BanView(
            [
                *state["remaining"],  # ty:ignore[not-iterable]
                NO_BAN
            ],
            callback_second_ban)

        await player2.send(generate_ban_message(player1,
                                                state["player1_ban_choice"]),
                           view=view,
                           silent=True)

    # 5: ask for confirmation
    async def callback_second_ban(interaction: discord.Interaction, selected):
        if (state["player2_ban_choice_made"]):
            await interaction.response.send_message(
                f"Vous avez déjà effectué votre bannissement contre {player1.name}"
            )
            return
        else:
            state["player2_ban_choice"] = selected
            await interaction.response.defer()

        await callback_confirm_second_ban()

    # 6: lock bans
    async def callback_confirm_second_ban():
        state["player2_ban_choice_made"] = True
        await ask_first_pick()

    # 7: ask for first pick
    async def ask_first_pick():
        if (state["player2_ban_choice"] != NO_BAN):
            state["remaining"].remove(  # ty:ignore[unresolved-attribute]
                state["player2_ban_choice"]  # ty:ignore[invalid-argument-type]
            )
        state["remaining"].append('Open et Standard')
        state["remaining"].append('Modes Exotiques')
        # pick view + send message
        valid_categories = {
            key: value
            for key, value in categories.items()
            if key in state["remaining"]  # ty:ignore[unsupported-operator]
        }
        view = PickView(valid_categories, callback_first_pick)

        await player1.send(generate_pick_message(player2, None),
                           view=view,
                           silent=True)

    # 8: ask for confirm
    async def callback_first_pick(interaction: discord.Interaction,
                                  selected: str):
        if (not state["player1_pick_choice"]):
            state["player1_pick_choice"] = selected
            await interaction.response.send_message("Merci mon chou")
        else:
            await interaction.response.send_message(
                "Vous avez déjà choisi un mode")
        await ask_second_pick(selected)

    # 10: ask second pick
    async def ask_second_pick(selected: str):
        # We might need to remove the selected mode, but it's for later
        valid_categories = {
            key: value
            for key, value in categories.items()
            if key in state["remaining"]  # ty:ignore[unsupported-operator]
        }
        view = PickView(valid_categories, callback_second_pick)

        await player2.send(generate_pick_message(player1,
                                                 state["player1_pick_choice"]),
                           view=view,
                           silent=True)

    # 11: ask for confirm
    async def callback_second_pick(interaction: discord.Interaction,
                                   selected: str):

        if (not state["player2_pick_choice"]):
            state["player2_pick_choice"] = selected
            await interaction.response.send_message("Merci mon chou")
        else:
            await interaction.response.send_message(
                "Vous avez déjà choisi un mode")

        await (roulette())

    #13: we might need a roulette
    async def roulette():
        await finalize()

    #14: send all information
    async def finalize():
        await result_channel.send(
            generate_banned_announcement_message(
                player1,
                player2,
                state[
                    "player1_ban_choice"],  # ty:ignore[invalid-argument-type]
                state["player2_ban_choice"]  # ty:ignore[invalid-argument-type]
            ))
        await result_channel.send(
            f"A L'ARRACHE, CA A PICK : {state['player1_pick_choice']} et {state['player2_pick_choice']}"
        )

    await ask_first_ban()


def generate_ban_message(opponent: discord.Member, opponent_choice=None):
    msg = f"""
    Bonjour à toi. Afin de planifier ton match contre {opponent.display_name},
    nous avons besoin que tu bannisses l'une des catégories. Si tu ne souhaites
    bannir aucune catégorie, c'est bien évidemment ton droit."""
    if opponent_choice:
        msg += f"""\n{"Ton adversaire n'a banni aucune catégorie" if opponent_choice == NO_BAN else f"Ton adversaire a banni la catégorie suivante : {opponent_choice}"}"""
    return msg


def generate_banned_announcement_message(player1: discord.Member,
                                         player2: discord.Member,
                                         player1_ban_choice: str | None,
                                         player2_ban_choice: str | None):
    return f"""
    Merci <@{player1.id}> et <@{player2.id}> d'avoir fini de bannir vos catégories.
    {player1.display_name} a choisi de {"**ne bannir aucun mode!**" if not player1_ban_choice else f"bannir le mode suivant : **{player1_ban_choice}**"}
    {player2.display_name} a choisi de {"**ne bannir aucun mode!**" if not player2_ban_choice else f"bannir le mode suivant : **{player2_ban_choice}**"}
    """


def generate_pick_message(opponent: discord.Member, opponent_choice=None):
    return "ENDIVE AU JAMBON"
