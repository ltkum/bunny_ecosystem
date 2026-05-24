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

|ENV_VAR               |fichier     |description                             |
|----------------------|------------|----------------------------------------|
|DISCORD_BOT_AUTH_TOKEN|.discord.env|token d'authentification de votre bot   |
|DISCORD_BOT_ROOT_NAME |.discord.env|le nom par lequel commence les commandes|
