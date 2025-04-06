# PiBot

A custom Discord bot for the Nu Deuteron chapter of Alpha Epsilon Pi.

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

Commands starting with / are accessible via slash commands, while the others are accessible via the application commands menu.

- `ask`: Ask a generative AI model a question.
- `Summarise`: Uses generative AI to summarise a message.
- `/dailyfact`: Shows a daily fact
- `/shipfact`: Uses generative AI to create a **fake** fact about ships
- `Describe`: Describe the contents of an image
- `Rate Meme`: Find out how good your meme is, and why
- `/info`: Shows some information about the bot
- `/help`: Shows help for the bot

### Admin Commands

Admin commands are not accessible through slash commands, and must be typed out as a normal message. Will only run if the user pertaining to `OWNER_ID` sends them.

- `/admin sync`: Syncs the bot's slash commands.
