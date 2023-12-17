import discord

from .discordenvs import COLOR


async def sync_slash_commands() -> list:
    embed = discord.Embed(
        title="Finished syncing slash commands",
        color=COLOR,
    )

    return [{"embed": embed, "view": None}]
