import os
import random

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
        url=message.jump_url,
    )

    return PiEmbed(embed=embed)


def image_response(text: str, image_url: str) -> list:
    return [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": text},
                {
                    "type": "input_image",
                    "image_url": image_url,
                    "detail": "low",
                },
            ],
        }
    ]


async def describe_image(message: discord.Message, url: str) -> PiEmbed:
    response = client.responses.create(model=MODEL, input=image_response("Describe this image in 1 sentence", url))

    embed = discord.Embed(
        title=f"Description of image sent by {message.author.name}",
        description=response.output_text,
        url=message.jump_url,
    )
    embed.set_thumbnail(url=url)

    return PiEmbed(embed=embed)


async def rate_meme(message: discord.Message, url: str) -> PiEmbed:
    rating = min(10, max(0, int(random.gauss(5, 2.5))))
    response = client.responses.create(
        model=MODEL,
        input=image_response(
            f"Explain why this meme is rated {rating} out of 10 in one sentence. Be as brutally honest as you can.", url
        ),
    )

    embed = discord.Embed(
        title=f"This meme from {message.author.name} is rated **{rating}/10**",
        description=response.output_text,
        url={message.jump_url},
    )
    embed.set_thumbnail(url=url)

    return PiEmbed(embed=embed)
