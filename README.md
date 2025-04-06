# PiBot

A custom AI-powered Discord bot for the Nu Deuteron chapter of Alpha Epsilon Pi.

## Setup

Create an `.env` file with the following keys:

```dotenv
TOKEN=Discord bot token
OPENAI=OpenAI API key
PREFIX=Prefix for the bot to use
OWNER_ID=Discord user id for admin command permission
```

Then install docker and docker compose and run the following command to start up the bot.

```shell
docker compose up -d
```

## Commands

Commands starting with `/` are accessible via slash commands, while the others are accessible via the application commands menu.

### AI Commands

The bot uses a local LLM running through ollama for simpler tasks and the ChatGPT API for more complex queries. Currently, the Microsoft's phi3 model is used locally.

#### Local LLM Commands

- `ask`: Ask a generative AI model a question.

#### ChatGPT Commands

- `Summarise`: Uses generative AI to summarise a message.
- `/shipfact`: Uses generative AI to create a **fake** fact about ships
- `Describe`: Describe the contents of an image
- `Rate Meme`: Find out how good your meme is, and why

### Other Commands

- `/dailyfact`: Shows the daily fact from [Joseph Paul's](https://uselessfacts.jsph.pl/) useless fact API
- `/info`: Shows some information about the bot
- `/help`: Shows help for the bot

### Admin Commands

Admin commands are not accessible through slash commands, and must be typed out as a normal message. Will only run if the user pertaining to `OWNER_ID` sends them.

- `/admin sync`: Syncs the bot's slash commands.
