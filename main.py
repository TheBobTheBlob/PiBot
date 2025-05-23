import os

import discord
from dotenv import load_dotenv

from components import admin, ai, embeds, misc
from components.exceptions import OllamaAPIError

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
    else:
        return

    kwargs = {"embed": result.embed}
    if result.view is not None:
        kwargs["view"] = result.view
    if result.file is not None:
        kwargs["file"] = result.file

    await message.channel.send(**kwargs)


# SLASH COMMANDS


@tree.command(name="info", description="Shows information about PiBot")
async def slash_info(interaction: discord.Interaction) -> None:
    result = await embeds.info_embed()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="help", description="Get help for PiBot commands")
async def slash_help(interaction: discord.Interaction) -> None:
    result = await embeds.help_embed(interaction.user.id == OWNER_ID)
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="dailyfact", description="Shows the fact of the day")
async def slash_dailyfact(interaction: discord.Interaction) -> None:
    result = await misc.dailyfact()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="shipfact", description="Get a random ship fact")
async def slash_shipfact(interaction: discord.Interaction) -> None:
    result = await ai.fake_ship_fact()
    await interaction.response.send_message(embed=result.embed)


@tree.command(name="ask", description="Ask PiBot a question")
async def test(interaction: discord.Interaction, question: str) -> None:
    await interaction.response.defer()
    try:
        result = await ai.ask_ollama(question)
    except OllamaAPIError:
        result = await embeds.error_embed("The local AI agent had an error. Please try again later.")
    await interaction.followup.send(embed=result.embed, ephemeral=result.ephemeral)


# CONTEXT MENU COMMANDS


@tree.context_menu(name="Summarise")
async def summarise(interaction: discord.Interaction, message: discord.Message):
    if len(message.content) < 5:
        result = await embeds.error_embed("Text too short to summarise")
    else:
        result = await ai.summarise(message)
    await interaction.response.send_message(embed=result.embed, ephemeral=result.ephemeral)


@tree.context_menu(name="Describe")
async def describe_image(interaction: discord.Interaction, message: discord.Message):
    if message.attachments:
        result = await ai.describe_image(message, message.attachments[0].url)
    else:
        result = await embeds.error_embed("No image found in the message")
    await interaction.response.send_message(embed=result.embed, ephemeral=result.ephemeral)


@tree.context_menu(name="Rate Meme")
async def rate_meme(interaction: discord.Interaction, message: discord.Message):
    if message.attachments:
        result = await ai.rate_meme(message, message.attachments[0].url)
    else:
        result = await embeds.error_embed("No image found in the message")
    await interaction.response.send_message(embed=result.embed, ephemeral=result.ephemeral)


# Start bot
client.run(TOKEN)
