import time
import discord
from discord import app_commands

HELP_INFORMATION = {
    "/lapin help": {
        "description":
        "Montre une liste des commandes utilisables sur le serveur",
        "is_restricted": False,
        "parameters": None,
        "example": "/lapin help"
    },
    "/lapin resultat": {
        "description": "Envoie le résultat du match sur un canal dédié",
        "is_restricted": False,
        "parameters": {
            "racetime_id": "l'id de la raceroom."
        },
        "example": "/lapin resultat wonderful-mushroom-22222"
    }
}


def format_one_help(key: str):
    if not HELP_INFORMATION.get(key, None):
        return ""
    toDisplay = []
    toDisplay.append(
        f"Commande: {key} **{'Fonction restreinte aux utilisateurs autorisés' if HELP_INFORMATION[key].get('is_restricted', True) else 'Fonction publique'}**"
    )
    toDisplay.append(f"{HELP_INFORMATION[key].get('description', '')}")
    if HELP_INFORMATION[key].get('parameters', None):
        toDisplay.append("\n**Paramètres**")
        for param_name, param_description in HELP_INFORMATION[key].get(
                'parameters', {}).items():
            toDisplay.append(f"{param_name}: {param_description}")
    toDisplay.append("\n**Exemple d'utilisation**")
    toDisplay.append(f"{HELP_INFORMATION[key].get('example', '')}")

    return "\n".join(toDisplay)


async def all_help_message(interaction: discord.Interaction):
    for key in HELP_INFORMATION.keys():

        await interaction.followup.send(format_one_help(key), ephemeral=True)
        time.sleep(2)


@app_commands.command(name="help")
async def send_help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Merci d'avoir demandé de l'aide, elle arrive gentillement",
        ephemeral=True)
    await all_help_message(interaction)
