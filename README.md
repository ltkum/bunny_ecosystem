# THE BUNNY ECOSYSTEM

Bonjour et bienvenue dans un projet un peu pourri que j'aime bien.

Le but est de créer un écosystème d'outils pour aider la communauté francophone de randomizer à gérer ses activités

Entre autre, il va comprendre un bot et une API discord, un bot (et certainement une API) rtgg, une base de donnée pour stocker les états et un frontend.

Pour le moment, on a juste commencé le bot discord.

## Installer le système

### Étape 1: ajouter les fichiers d'environnement

à la racine du projet

```touch  .discord.env```

dans ce fichier d'environnement, ajoutez

```.env
DISCORD_BOT_AUTH_TOKEN="VOTRE TOKEN PERSONNEL. (si vous l'ajoutez sur github, vous êtes un peu cons)"
DISCORD_BOT_ROOT_NAME="exemple"
```

### Étape 2: build

``` bash
docker compose build
```

### Étape 3: lancer

```bash
docker compose up -d
```

### Étape 4: stopper le bot

```bash
docker compose down
```

### Variables d'environnement et utilité

#### Seules la première est obligatoire. Les autres vont simplement bloquer des fonctionalités de configurations initiales

|ENV_VAR                          |fichier     |description                                                       |
|---------------------------------|------------|------------------------------------------------------------------|
|DISCORD_BOT_AUTH_TOKEN           |.discord.env|token d'authentification de votre bot                             |
|DISCORD_BOT_ROOT_NAME            |.discord.env|le nom par lequel commence les commandes                          |
|GOOGLE_SCRIPT_SCHEDULE_LINK      |.discord.env|le lien vers le script d'aggrégation de données de l'horaire ZSRFR|
|ZSFR_SIGNUP_SHEET                |.discord.env|le lien vers la feuille d'inscriptions bénévoles de ZSRFR         |
|TEST_SERVER_ID                   |.discord.env|ID de votre serveur de test                                       |
|TEST_SERVER_CREW_CHANNEL_ID      |.discord.env|ID initiale du channel d'équipe de restream du serveur de test    |
|TEST_SERVER_BO_CHANNEL_ID        |.discord.env|ID initiale du channel des BO du serveur de test                  |
|TEST_SERVER_BO_ROLE_ID           |.discord.env|ID du role de BO sur le serveur de test                           |
|TEST_SERVER_TRACK_ROLE_ID        |.discord.env|ID du role de BO sur le serveur de test                           |
|TEST_SERVER_COMM_ROLE_ID         |.discord.env|ID du role de BO sur le serveur de test                           |
|FFSFR_SERVER_ID                  |.discord.env|ID du serveur franco                                              |
|FFSFR_SERVER_DASHBOARD_CHANNEL_ID|.discord.env|ID initiale du channel d'équipe de restream du serveur franco     |
|FFSFR_SERVER_BO_CHANNEL_ID       |.discord.env|ID initiale du channel des BO du serveur franco                   |
|FFSFR_SERVER_CREW_CHANNEL_ID     |.discord.env|ID initiale du channel d'équipe de restream du serveur franco     |
|FFSFR_SERVER_BO_ROLE_ID          |.discord.env|ID du role de BO sur le serveur franco                            |
|FFSFR_SERVER_TRACK_ROLE_ID       |.discord.env|ID du role de BO sur le serveur franco                            |
|FFSFR_SERVER_COMM_ROLE_ID        |.discord.env|ID du role de BO sur le serveur franco                            |

### Restrictions du Bot

Le bot est pour le moment prévu pour fonctionner dans un environnement précis. À savoir, fournir quelques fonctionalités très spécifiques pour la communauté francophone de randomizer A link to the Past.

Certaines de ses fonctionalités ne sont pas configurables, et utilisent donc des variables d'environnement spécifiques. Il sera possible, sur le long terme, de changer ça et d'assigner des variables là où c'est nécessaire, mais pour le moment, partez du principe que les différentes fonctionalités ne sont utilisable que sur le serveur discord de la communauté de rando alttp francophone.

### Commandes utilisables par le bot

#### Commandes utilisables par n'importe quel membre

`/lapin resultat racetime_room_id` : envoie sur le dashboard le résultat du match contenu dans la race room définie.

#### Commandes demandant des privilèges

Les différentes commandes ici peuvent être utilisées soit par un admin, soit par une personne/un rôle qui a reçu le privilège de le faire par un admin.

`/lapin tournament initialize config.json`: transforme la configuration donnée en structure de tournoi.

`/lapin restream ask_for_bo`: vérifie l'horaire ZSRFR et envoie dans le canal des BO la liste des matches qui n'ont pas encore de BO dans les 7 prochains jours

`/lapin restream ask_for_crew`: vérifie l'horaire ZSRFR et envoie dans le canal de recherche d'équipe de restream la liste des matches qui ont un BO, mais pas tous les commentateurs / traqueurs dans les 7 prochains jours.

`/lapin admin set_dashboard_channel text_channel`: définit le canal de texte en paramètre comme étant le nouveau dashboard

`/lapin admin set_bo_channel text_channel`: définit le canal de texte en paramètre comme étant le nouveau canal des BO

`/lapin admin set_crew_channel text_channel`: définit le canal de texte en paramètre comme étant le nouveau canal des équipes de restream

#### Commandes ne pouvant être réalisées que par un administrateur serveur

`/lapin sudo set_permissions config.json` : accorde des droits d'utilisation du bot aux rôles spécifiés dans la configuration.

#### Détails

La décision de mettre en place des variables d'environnement pour les channels d'organisation des tournois, et des rôles liés, vient du fait que celà réduit l'intervention humaine nécessaire pour remettre en place le bot après une panne ou un arrêt. Sur le long terme, nous comptons installer une base de donnée afin d'avoir de la persistance et permettre au bot de récupérer de lui même ses configurations.

#### Roadmap ?

Non.

Mais en gros, ce que nous allons produire

**Futur Proche**: gestion basique des weekly, créations de canaux et autres pour les brackets

**Moyen Terme**: base de donnée pour la persistance des configurations et des événements. Création basique de race rooms et récupération automatique des résultats.

**Long Terme**: automatisation des phases de picks et bans des tournois, automatisation des weeklys, gestion complète des tournois

**Des idées ?**: Ben en vrai, demandez hein, on sait jamais.
