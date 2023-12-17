import os

import discord
from dotenv import load_dotenv

from components import misc, mtg

load_dotenv()
PREFIX = os.getenv("PREFIX")
DEV_ID = os.getenv("DEV_ID")

# Discord.py setup

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    match message.content.strip():
        case m if "[[" in m:
            responses = await mtg.card_brackets(message.content)
        case m if m.startswith(f"{PREFIX}card "):
            responses = await mtg.card_cmd(message.content)
        # case m if m == f"{PREFIX}sync":
        #     if message.author.id == int(DEV_ID):
        #         await tree.sync()
        #         responses = await misc.sync_slash_commands()
        #     else:
        #         return
        case _:
            return

    for response in responses:
        if response["view"] is None:
            await message.channel.send(embed=response["embed"])
        else:
            await message.channel.send(embed=response["embed"], view=response["view"])


@tree.command(name="test", description="Shows the server rules")
async def rules(interaction: discord.Interaction) -> None:
    rules = (
        "1. Don't say bad words",
        "2. Respect other people",
        "3. You mustn't speak loud in voice channels",
    )

    await interaction.response.send_message(f"{rules}")


# Get TOKEN and start bot

if (TOKEN := os.getenv("TOKEN")) is not None:
    client.run(TOKEN)
else:
    print("Environment variable TOKEN not set")
