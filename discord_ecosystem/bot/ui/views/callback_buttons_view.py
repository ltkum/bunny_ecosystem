from dataclasses import dataclass, field
from typing import Callable, Any

from functools import partial

import discord


@dataclass
class ButtonDefinition:

    label: str

    callback: Callable

    kwargs: dict[str, Any] = field(default_factory=dict)

    style: discord.ButtonStyle = (discord.ButtonStyle.blurple)

    disabled: bool = False

    row: int | None = None


class CallbackButtonView(discord.ui.View):

    def __init__(self, buttons: list[ButtonDefinition], *args, **kwargs):

        super().__init__(*args, **kwargs)

        for definition in buttons:

            button = discord.ui.Button(label=definition.label,
                                       style=definition.style,
                                       disabled=definition.disabled,
                                       row=definition.row)

            button.callback = partial(self._dispatch, definition.callback,
                                      definition.kwargs, button)

            self.add_item(button)

    async def _dispatch(self, callback: Callable, kwargs: dict[str, Any],
                        button: discord.ui.Button,
                        interaction: discord.Interaction):
        button.disabled = kwargs.get('disable_button', False)
        await interaction.response.send_message(kwargs["message"])
        await callback(interaction=interaction, button=button, **kwargs)
