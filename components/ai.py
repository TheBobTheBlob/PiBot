import os

import discord
from openai import OpenAI

from .embeds import PiEmbed

OPENAI_KEY = os.environ["OPENAI"]

MODEL = "gpt-4o-mini"

client = OpenAI(api_key=OPENAI_KEY)


async def fake_ship_fact() -> PiEmbed:
    response = client.responses.create(model=MODEL, input="Give me a one-sentence fake fact about ships")

    embed = discord.Embed(
        title="Ship Fact",
        description=response.output_text,
    )

    return PiEmbed(embed=embed)


async def summarise(message: discord.Message) -> PiEmbed:
    sentences = 1

    response = client.responses.create(
        model=MODEL,
        instructions=f"Summarise this message in {sentences} sentences",
        input=message.content,
    )

    embed = discord.Embed(
        title=f"Summary for {message.author.name}'s message",
        description=response.output_text,
    )

    return PiEmbed(embed=embed)
