# 🤖 Discord Bot

<div align="center">

![Python](https://img.shields.io/badge/python-3.11_|_3.12-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-package_manager-blue)
![Discord.py](https://img.shields.io/badge/discord.py-2.4.0-blue)
![License](https://img.shields.io/badge/license-GPL_3.0-green)
[![Code style: black](https://img.shields.io/badge/code_style-black-black)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/ruff-linter-red)](https://github.com/astral-sh/ruff)

Un bot Discord moderne et modulaire avec une architecture propre et des outils de développement de pointe.

</div>

## 🌟 Fonctionnalités

- 🎨 **Commandes YouTube** - Créez des aperçus de miniatures YouTube personnalisées
- 🛠️ **Modération** - Outils de modération essentiels pour votre serveur
- 📊 **Création d'Embeds** - Interface intuitive pour créer des embeds Discord

## 🏗️ Architecture

```
discord-bot/
├── api/                    # API REST (future implementation)
├── assets/                 # Ressources statiques
├── cogs/                   # Modules de commandes Discord
├── infrastructure/         # Services et utilitaires
│   └── services/
│       ├── cog_loader.py   # Chargeur automatique de cogs
│       └── logger_service.py # Service de logging
├── logs/                   # Fichiers de logs
├── .env                    # Variables d'environnement
├── main.py                # Point d'entrée de l'application
└── pyproject.toml         # Configuration du projet
```

## 🚀 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

2. **Installer Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Installer les dépendances**
```bash
poetry install
```

4. **Configurer les variables d'environnement**
```bash
cp .env.sample .env
# Éditer .env avec vos tokens et configurations
```

## 💻 Développement

### Outils de développement

- **Poetry** - Gestionnaire de dépendances
- **Black** - Formateur de code
- **Ruff** - Linter Python ultra-rapide
- **Pre-commit** - Hooks de pré-commit pour la qualité du code

### Commandes utiles

```bash
# Lancer le bot en mode développement
make dev

# Formater le code
make format

# Lancer avec Docker
make run
```

### Docker

Le projet inclut une configuration Docker pour le développement :

```bash
# Lancer avec Docker Compose
docker compose -f docker-compose.dev.yml up --build
```

## 🔧 Configuration

Le bot utilise `pydantic-settings` pour une gestion robuste de la configuration :

```python
# .env
DISCORD_TOKEN=votre_token_discord
```

## 📝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Distribué sous la licence GPL 3.0. Voir `LICENSE` pour plus d'informations.

## ✨ Remerciements

- [discord.py](https://github.com/Rapptz/discord.py)
- [Poetry](https://python-poetry.org/)
- [Ruff](https://github.com/astral-sh/ruff)
- [Black](https://github.com/psf/black)