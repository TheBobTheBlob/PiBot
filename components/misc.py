import aiohttp
import discord

from .embeds import PiEmbed


async def dailyfact() -> PiEmbed:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/api/v2/facts/today?language=en") as resp:
            fact = await resp.json()

    embed = discord.Embed(title="Daily Fact", description=fact["text"])
    embed.set_footer(text=f"Source: {fact['source']}")

    return PiEmbed(embed=embed)
