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
