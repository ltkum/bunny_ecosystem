import discord
from bot.ui.views.confirm_view import SimpleConfirmView
from common.actions.get_user import get_member_by_id
from bot.commands.tournament.launch.steps.generate_structure import generate_structure


async def confirm_config(interaction: discord.Interaction,
                         guild: discord.Guild, data: dict):
    view = SimpleConfirmView(generate_structure, guild=guild, data=data)

    msg = "Merci de vérifier que les groupes soient corrects :3 \n"
    msg += '\n'.join(
        [group_to_string(group, guild) for group in data["groups"]])
    await interaction.followup.send(msg, view=view)


def group_to_string(group: dict, guild: discord.Guild):
    members_name: list[str] = [
        get_member_by_id(guild, id).name for id in group["players"]
    ]
    return f"**{group['role_name']}** : {', '.join(members_name)}"
