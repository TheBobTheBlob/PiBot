import discord

from .discordenvs import COLOR


async def sync_slash_commands(tree) -> list:
    await tree.sync()
    embed = discord.Embed(
        title="Synced slash commands",
        color=COLOR,
    )

    return [{"embed": embed, "view": None}]
