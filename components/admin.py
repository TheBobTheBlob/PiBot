import discord

from .embeds import PREFIX, PiEmbed


async def admin_commands(message: discord.Message, **kwargs) -> PiEmbed:
    command = message.content.lower().strip().strip(f"{PREFIX}admin ")

    match command:
        case "sync":
            embed = await sync_slash_commands(**kwargs)
        case "":
            embed = discord.Embed(title="No command given")
        case _:
            embed = discord.Embed(title=f'Invalid admin command "{command}"')

    return PiEmbed(embed=embed)


async def sync_slash_commands(tree: discord.app_commands.CommandTree) -> discord.Embed:
    await tree.sync()
    embed = discord.Embed(title="Synced slash commands")

    return embed
