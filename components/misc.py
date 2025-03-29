from dataclasses import dataclass

import aiohttp
import discord

from .embeds import PREFIX, PiEmbed


async def info_embed() -> PiEmbed:
    embed = discord.Embed(
        title="PiBot Information",
        description="PiBot is a custom bot for the Nu Deuteron chapter of Alpha Epsilon Pi",
    )

    file = discord.File("static/logo.jpg", filename="logo.jpg")
    embed.set_thumbnail(url="attachment://logo.jpg")

    embed.add_field(name="Repository", value="https://github.com/TheBobTheBlob/PiBot")
    embed.add_field(name="Birthday", value="December 13, 2023")

    return PiEmbed(embed=embed, file=file)


@dataclass
class CommandHelp:
    name: str
    description: str


@dataclass
class CommandCategory:
    name: str
    description: str
    commands: list[CommandHelp]
    for_admin: bool = False


commands = [
    CommandCategory(
        "Facts",
        "Commands that give you a fact.",
        commands=[
            CommandHelp(name="dailyfact", description="Shows the fact of the day"),
            CommandHelp(name="shipfact", description="Get a random **fake** ship fact generated by AI"),
        ],
    ),
    CommandCategory(
        name="Miscellaneous",
        description="Other commands available to use.",
        commands=[
            CommandHelp(name="info", description="Shows basic information about this bot"),
            CommandHelp(name="help", description="Shows this help message"),
        ],
    ),
    CommandCategory(
        name="Admin",
        description="Commands for the bot administrator.",
        commands=[
            CommandHelp(name="admin sync", description="Sync slash commands"),
        ],
        for_admin=True,
    ),
]


async def help_embed(is_admin: bool) -> PiEmbed:
    embed = discord.Embed(title="PiBot Help")

    for category in commands:
        if category.for_admin and not is_admin:
            continue

        text = category.description

        for command in category.commands:
            text += f"\n- `{PREFIX}{command.name}` {command.description}"

        embed.add_field(name=category.name, value=text)

    return PiEmbed(embed=embed)


async def dailyfact() -> PiEmbed:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/api/v2/facts/today?language=en") as resp:
            fact = await resp.json()

    embed = discord.Embed(title="Daily Fact", description=fact["text"])
    embed.set_footer(text=f"Source: {fact['source']}")

    return PiEmbed(embed=embed)
