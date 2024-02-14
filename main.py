import os
from typing import Literal, Optional

import discord
from dotenv import load_dotenv

from components import admin, events, misc, mtg
from components.discordenvs import PiEmbed, PiList
from database import oracle

load_dotenv()

PREFIX = os.environ["PREFIX"]
OWNER_ID = os.environ["OWNER_ID"]
TOKEN = os.environ["TOKEN"]


# DISCORD.PY SETUP


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# DISCORD.PY EVENTS


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    is_admin = message.author.id == int(OWNER_ID)
    text = message.content.strip()

    if "[[" in text:
        result = await mtg.card_brackets(message.content)
    elif text.startswith(f"{PREFIX}card "):
        result = await mtg.card_cmd(message.content)
    elif text.startswith(f"{PREFIX}admin") and is_admin:
        result = await admin.admin_commands(message.content, tree=tree)
    elif text == f"{PREFIX}dailyfact":
        result = await misc.dailyfact()
    elif text.startswith(f"{PREFIX}info"):
        result = await misc.info_embed()
    elif text.startswith(f"{PREFIX}help"):
        result = await misc.help_embed(is_admin)
    else:
        return

    if isinstance(result, PiEmbed):
        await message.channel.send(embed=result.embed, view=result.view, file=result.file)
    elif isinstance(result, PiList):
        for embed in result.get_all():
            await message.channel.send(embed=embed.embed, view=embed.view, file=embed.file)


@client.event
async def on_scheduled_event_create(event) -> None:
    setting = await oracle.annouce_creation(event.guild.id)

    if setting:
        result = events.event_created_card(event)
        channel = await client.fetch_channel(await oracle.annoucement_channel(event.guild.id))

        message = await channel.send(embed=result.embed)
        await message.add_reaction("✅")
        await message.add_reaction("❎")


# SLASH COMMANDS


# TODO MTG Price subcommand
@tree.command(name="card", description="Search for an MTG card")
@discord.app_commands.describe(name="Name of the MTG card", kind="Specify what the command returns")
async def slash_card(
    interaction: discord.Interaction, name: str, kind: Optional[Literal["image", "price"]] = "image"
) -> None:
    if kind == "price":
        result = await mtg.card_slash(name)
    else:
        result = await mtg.card_slash(name)

    if result.view is None:
        await interaction.response.send_message(embed=result.embed)
    else:
        await interaction.response.send_message(embed=result.embed, view=result.view)


@tree.command(name="info", description="Shows information about PiBot")
async def slash_info(interaction: discord.Interaction) -> None:
    result = await misc.info_embed()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="help", description="Get help for PiBot commands")
async def slash_help(interaction: discord.Interaction) -> None:
    result = await misc.help_embed(interaction.user.id == int(OWNER_ID))
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="dailyfact", description="Shows the fact of the day")
async def slash_dailyfact(interaction: discord.Interaction) -> None:
    result = await misc.dailyfact()
    await interaction.response.send_message(embed=result.embed)


# Start bot
client.run(TOKEN)
