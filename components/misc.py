import discord

from .discordenvs import COLOR, PREFIX, PiEmbed


async def sync_slash_commands(tree) -> list[PiEmbed]:
    await tree.sync()
    embed = discord.Embed(
        title="Synced slash commands",
        color=COLOR,
    )

    return [PiEmbed(embed=embed)]


async def info_embed() -> list[PiEmbed]:
    embed = discord.Embed(
        title="PiBot Information",
        description="PiBot is a custom bot for the Nu Deuteron chapter of Alpha Epsilon Pi",
        color=COLOR,
    )

    file = discord.File("static/logo.jpg", filename="logo.jpg")
    embed.set_thumbnail(url="attachment://logo.jpg")

    embed.add_field(name="Repository", value="https://github.com/TheBobTheBlob/PiBot")
    embed.add_field(name="Birthday", value="December 13, 2023")

    return [PiEmbed(embed=embed, file=file)]


async def help_embed() -> list[PiEmbed]:
    embed = discord.Embed(title="PiBot Help", color=COLOR)

    # Have to use \n and not newlines, as those render as sublists on Discord
    embed.add_field(
        name="MTG Cards",
        value=f"""Shows images of MTG cards. Data is taken from Scryfall. There are three ways to call this command.

    - `[[name]]` Surround the card name in double square brackets\n- `{PREFIX}card name` Use the card command with the prefix "{PREFIX}"\n- `/card name` Use the card slash command\n
    """,
    )

    embed.add_field(
        name="Miscellaneous",
        value=f"""Other commands available to use.
    
    - `{PREFIX}info` Shows basic information about this bot\n- `{PREFIX}help` Shows this help message""",
    )

    return [PiEmbed(embed=embed)]
