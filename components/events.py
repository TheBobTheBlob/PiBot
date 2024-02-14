import discord

from .discordenvs import PiEmbed


def event_created_card(event: discord.ScheduledEvent) -> PiEmbed:
    embed = discord.Embed(
        title=f"{event.name}", description="A new event has been created. React whether you can attend or not."
    )

    if event.description:
        embed.add_field(name="Description", value=event.description)

    embed.add_field(
        name="Time",
        value=f"Starts: <t:{int(event.start_time.timestamp())}>\nEnds:᲼ <t:{int(event.end_time.timestamp())}>",  # Invisible character to align the times
    )

    if event.location:
        embed.add_field(name="Location", value=event.location)

    return PiEmbed(embed=embed)
