# PiBot

A custom bot for the Nu Deuteron chapter of Alpha Epsilon Pi.

## Setup

This bot uses `discord.py`, `python-dotenv` and `openai`. After installing these packages, create an `.env` file with the following keys:

```dotenv
TOKEN=Discord bot token
OPENAI=OpenAI API key
PREFIX=Prefix for the bot to use
OWNER_ID=Discord user id for admin command permission
```

Then, install docker and run the following commands to create a container and run it.

```shell
docker build -t discord-bot .
```

```shell
docker run  --env-file .env -d discord-bot
```

## Commands

All commands must be prefixed with the prefix if used in a message, or are accessible through Discord's slash commands.

- `summarise`: Uses generative AI to summarise a message. Awailable through messages or the context menu.
- `dailyfact`: Shows a daily fact
- `shipfact`: Uses generative AI to create a **fake** fact about ships
- `info`: Shows some information about the bot
- `help`: Shows help for the bot

### Admin Commands

Admin commands are not accessible through slash commands.

- `admin sync`: Syncs the bot's slash commands.
