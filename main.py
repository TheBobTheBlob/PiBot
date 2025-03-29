import os

import discord
from dotenv import load_dotenv

from components import admin, ai, misc

load_dotenv()

PREFIX = os.environ["PREFIX"]
OWNER_ID = int(os.environ["OWNER_ID"])
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
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    is_admin = message.author.id == OWNER_ID
    text = message.content.strip().lower()

    if text.startswith(f"{PREFIX}admin") and is_admin:
        result = await admin.admin_commands(message, tree=tree)
    elif text == f"{PREFIX}dailyfact":
        result = await misc.dailyfact()
    elif text.startswith(f"{PREFIX}info"):
        result = await misc.info_embed()
    elif text.startswith(f"{PREFIX}help"):
        result = await misc.help_embed(is_admin)
    elif text.startswith(f"{PREFIX}shipfact"):
        result = await ai.fake_ship_fact()
    else:
        return

    await message.channel.send(embed=result.embed, view=result.view, file=result.file)


# SLASH COMMANDS


@tree.command(name="info", description="Shows information about PiBot")
async def slash_info(interaction: discord.Interaction) -> None:
    result = await misc.info_embed()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="help", description="Get help for PiBot commands")
async def slash_help(interaction: discord.Interaction) -> None:
    result = await misc.help_embed(interaction.user.id == OWNER_ID)
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="dailyfact", description="Shows the fact of the day")
async def slash_dailyfact(interaction: discord.Interaction) -> None:
    result = await misc.dailyfact()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="shipfact", description="Get a random ship fact")
async def slash_shipfact(interaction: discord.Interaction) -> None:
    result = await ai.fake_ship_fact()
    await interaction.response.send_message(embed=result.embed)


# Start bot
client.run(TOKEN)
