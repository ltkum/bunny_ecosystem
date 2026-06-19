"""
    This file will handle command permissions.
    The GUILD_PERMISSIONS will be a dict which is in the following structure
    {
        GUILD_ID: {
            group_name: [array_of, allowed, role_ids],
            group_name_2: [same]
        }
    }

    When database is in place, we should add a function to make the db call
"""
import discord
from discord import app_commands

GUILD_PERMISSIONS: dict[int, dict[str, list[int]]] = {}


# TODO URGENT: documenter la structure des permissions
def load_guild_config(guild_id: int, data: dict):
    GUILD_PERMISSIONS[guild_id] = data


def has_permission(interaction: discord.Interaction, group: str) -> bool:

    guild_id = interaction.guild_id
    if not guild_id or not isinstance(interaction.user, discord.Member):
        return False

    # admin bypass
    if interaction.user.guild_permissions.administrator:
        return True

    # if there is at least one role id which is both in the user roles and in the permission
    # the command is allowed
    return bool({role.id
                 for role in interaction.user.roles}.intersection(
                     GUILD_PERMISSIONS.get(guild_id, {}).get(group, [])))


def requires_group(group: str):

    async def predicate(interaction: discord.Interaction):

        if has_permission(interaction, group):
            return True
        await interaction.response.send_message(
            "Vous n'avez pas le niveau d'accréditation requis, citoyen.ne")
        raise app_commands.CheckFailure(f"No permission for group: {group}")

    return app_commands.check(predicate)
