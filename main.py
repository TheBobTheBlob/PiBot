import os
import sys
from typing import Literal, Optional

import discord
from dotenv import load_dotenv

from components import misc, mtg

load_dotenv()
if (PREFIX := os.getenv("PREFIX")) is None:
    print("Environmental variable PREFIX not set")
    sys.exit(1)
if (OWNER_ID := os.getenv("OWNER_ID")) is None:
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

    text = message.content.strip()

    if "[[" in text:
        responses = await mtg.card_brackets(message.content)
    elif text.startswith(f"{PREFIX}card "):
        responses = await mtg.card_cmd(message.content)
    elif text == f"{PREFIX}sync":
        if message.author.id == int(OWNER_ID):
            responses = await misc.sync_slash_commands(tree)
        else:
            return
    elif text.startswith(f"{PREFIX}info"):
        responses = await misc.info_embed()
    elif text.startswith(f"{PREFIX}help"):
        responses = await misc.help_embed()
    else:
        return

    for response in responses:
        await message.channel.send(embed=response.embed, view=response.view, file=response.file)


# SLASH COMMANDS


@tree.command(name="card", description="Search for an MTG card")
@discord.app_commands.describe(name="Name of the MTG card", send="Specify what the command returns")
async def slash_card(
    interaction: discord.Interaction, name: str, send: Optional[Literal["image", "price"]] = "image"
) -> None:
    if send == "price":
        responses = await mtg.card_slash(name)
    else:
        responses = await mtg.card_slash(name)

    if responses[0].view is None:
        await interaction.response.send_message(embed=responses[0].embed)
    else:
        await interaction.response.send_message(embed=responses[0].embed, view=responses[0].view)


@tree.command(name="info", description="Shows information about PiBot")
async def slash_info(interaction: discord.Interaction) -> None:
    responses = await misc.info_embed()
    await interaction.response.send_message(embed=responses[0].embed)


@tree.command(name="help", description="Get help for PiBot commands")
async def slash_help(interaction: discord.Interaction) -> None:
    responses = await misc.help_embed()
    await interaction.response.send_message(embed=responses[0].embed)


# GET TOKEN AND START BOT

if (TOKEN := os.getenv("TOKEN")) is not None:
    client.run(TOKEN)
else:
    print("Environment variable TOKEN not set")
    sys.exit(1)
