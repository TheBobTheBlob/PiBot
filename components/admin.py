import discord

from database import oracle

from .discordenvs import PREFIX, PiEmbed


async def admin_commands(message, **kwargs) -> PiEmbed:
    command = message.strip(f"{PREFIX}admin ")

    match command:
        case "sync":
            embed = await sync_slash_commands(**kwargs)
        case "events config":
            embed = await events_config(message)
        # case "" | "help":
        #     embed = await admin_help()
        case _:
            embed = discord.Embed(title=f'Invalid admin command "{command}"')

    return PiEmbed(embed=embed)


async def sync_slash_commands(tree) -> discord.Embed:
    await tree.sync()
    embed = discord.Embed(title="Synced slash commands")

    return embed


async def events_config(message) -> discord.Embed:
    command = message.strip(f"{PREFIX}admin events config ")
    await oracle.new_event_config(message.guild.id, command.split(" ")[0], command.split(" ")[1])

    embed = discord.Embed(title="Configured events for this server")
    return embed


# TODO Admin help command
async def admin_help():
    pass
