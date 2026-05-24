import time
import discord
from discord import app_commands

HELP_INFORMATION = {
    "/lapin help": {
        "description":
        "Montre une liste des commandes utilisables sur le serveur",
        "is_restricted": False,
        "parameters": None,
        "example": "/help"
    },
    "/lapin allow": {
        "description":
        "Authorise un rôle à effectuer une commande sur le serveur",
        "is_restricted": True,
        "parameters": {
            "role":
            "Le nom du rôle qui va recevoir l'authorisation d'utiliser une commande",
            "command": "Le nom de la commande qui va être authorisée"
        },
        "example": "/allow admin_team allow"
    },
    "/lapin revoke": {
        "description":
        "révoque l'authorisation d'un rôle à utiliser une commande sur le serveur",
        "is_restricted": True,
        "parameters": {
            "role":
            "Le nom du rôle qui n'aura plus l'autorisation d'utiliser une commande",
            "command": "Le nom de la commande interdite"
        },
        "example": "/revoke role=admin_team command=allow"
    },
    "/lapin launch_tournament": {
        "description":
        "Crée les canaux de groupes, les rôles et lance la phase de pick / ban pour les participants au tournoi",
        "is_restricted": True,
        "parameters": {
            "config_file":
            "un fichier JSON qui contient les informations nécessaires à lancer le tournoi.",
        },
        "example": "/launch_tournament [tournoi_2026.json]"
    },
    "/lapin clean_tournament": {
        # idéalement, ça devrait aussi stopper toute interaction liée au tournoi en particulier de fonctionner.
        "description":
        "Fait le cleanup d'un tournoi en enlevant les groupes, retirant les rôles aux participants, et archivant les canaux de discussions de groupes.",
        "is_restricted": True,
        "parameters": {
            "config_file":
            "Le même fichier de configuration que pour créer le tournoi",
        },
        "example": "/clean_tournament [tournoi_2026.json]"
    },
    "/lapin launch_brackets_round": {
        "description":
        "Crée des threads d'organisation pour chaque paire de la ronde en cours, et lance une phase de pick/ban",
        "is_restricted": True,
        "parameters": {
            "config_file":
            "Un fichier JSON qui contient le nom de la catégorie et les paires de joueurs",
        },
        "example": "/launch_brackets_round [brackets_1.json]"
    },
    "/lapin launch_weekly_loop": {
        "description":
        "Planifie et donne les éléments d'interactions pour la génération de la prochaine weekly. Va créer l'événement, et donner Quatre boutons pour gérer la weekly. L'un d'eux permet de lancer la gestion des restreams, Le second d'envoyer le message qui annonce le début de la weekly, le troisième va lancer la petite boucle pour montrer la raceroom, le dernier clôt le chapitre et restaure l'état de la weekly à son état original.",
        "is_restricted":
        True,
        "parameters": {
            "discord_command":
            "la commande à utiliser sur discord pour générer une seed d'entraînement",
            "rtgg_command": "la commande à utiliser dans la raceroom ",
            "description": "Une description du mode de la prochaine weekly",
        },
        "example":
        "/launch_weekly_loop '/preset open' '!race open' 'Ben c'est une open quoi'",
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
