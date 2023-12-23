import os
import sys

import discord
from dotenv import load_dotenv

from components import misc, mtg

load_dotenv()
if (PREFIX := os.getenv("PREFIX")) is None:
    print("Environmental variable PREFIX not set")
    sys.exit(1)
if (OWNER_ID := os.getenv("TOKEN")) is None:
    print("Environment variable OWNER_ID not set")
    sys.exit(1)


# DISCORD.PY SETUP

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
        case m if m == f"{PREFIX}sync":
            if message.author.id == int(OWNER_ID):
                responses = await misc.sync_slash_commands(tree)
            else:
                return
        case _:
            return

    for response in responses:
        responses = await mtg.card_cmd(message.content)
        if response["view"] is None:
            await message.channel.send(embed=response["embed"])
        else:
            await message.channel.send(embed=response["embed"], view=response["view"])


# SLASH COMMANDS


@tree.command(name="card", description="Search for an MTG card")
async def slash_card(interaction: discord.Interaction, name: str) -> None:
    responses = await mtg.card_slash(name)

    if responses[0]["view"] is None:
        await interaction.response.send_message(embed=responses[0]["embed"])
    else:
        await interaction.response.send_message(embed=responses[0]["embed"], view=responses[0]["view"])


# GET TOKEN AND START BOT

if (TOKEN := os.getenv("TOKEN")) is not None:
    client.run(TOKEN)
else:
    print("Environment variable TOKEN not set")
    sys.exit(1)
