import discord
import json

from common.actions.get_category_from_server_by_id import get_category_by_id


async def can_we_start_tournament(interaction: discord.Interaction,
                                  guild: discord.Guild,
                                  json_config: discord.Attachment):
    """ This function should
            1. check if the state allows for the tournament to start
            2. validate the data

            since this is a server-only command, we know discord.guild exists
        Args:
            data | None: the validated config as a dict
        """

    is_config_falsy, cfg_validation_msg, data = await validate_and_return_json_config(
        json_config, guild)
    await interaction.followup.send(cfg_validation_msg, ephemeral=True)
    if not data or is_config_falsy:
        await interaction.followup.send("Annulation de la création du tournoi",
                                        ephemeral=True)
        return None
    return data


async def validate_and_return_json_config(json_file: discord.Attachment,
                                          guild: discord.Guild):
    """Validate a JSON and returns the configuration it represents if it's valid.

    Args:
        json_file (discord.Attachment): a JSON file
        guild (discord.Guild): the guild in which we are running the command

    Returns:
        bool, str, data: a boolean telling us if the validation was successful, a validation message, and the configuration
    """
    is_falsy = False
    issues = []
    try:
        data = json.loads(await json_file.read())
        if not isinstance(data, dict):
            return True, "Le fichier reçu n'est pas un JSON valide", None
        if not isinstance(data.get("category_id", None),
                          int) or not get_category_by_id(
                              guild, data["category_id"]):
            issues.append(
                "category_id doit être présente et doit être une ID de catégorie présente sur le serveur"
            )
            is_falsy = True
        if not isinstance(data.get("general_role_name", None), str):
            issues.append(
                "general role name doit être une chaîne de caractère")
            is_falsy = True
        if not isinstance(data.get("groups", None), list) or len(
                data["groups"]) == 0:
            issues.append(
                "Il doit y avoir un champ 'groups' qui contient au moins un objet"
            )
            is_falsy = True
        else:
            for group in data["groups"]:
                if not (isinstance(group, dict)):
                    is_falsy = True
                    issues.append("Chaque groupe doit être un objet")
                else:
                    if not isinstance(group.get("role_name", None), str):
                        issues.append(
                            "Le champ 'role_name' doit être présent dans un groupe et être une chaîne de caractères"
                        )
                        is_falsy = True
                    if not isinstance(group.get("players", None), list):
                        issues.append(
                            "Le champ 'players' doit être une liste d'entiers représentants les ID des joueurs"
                        )
                        is_falsy = True
                    elif len([
                            playerid for playerid in group["players"]
                            if isinstance(playerid, int)
                    ]) < len(group["players"]):
                        is_falsy = True
                        issues.append(
                            "Tous les ids d'un des groupes ne sont pas des entiers"
                        )

        return is_falsy, format_msg(issues), data
    except Exception as e:
        return True, "Quelque chose a foiré :3", None


def format_msg(components: list[str]):

    return "\n".join(components) if len(
        components
    ) > 0 else "Aucune erreur trouvée dans le JSON de configuration"
