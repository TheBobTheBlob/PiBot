import logging
import os
import random

import aiohttp
import discord
from openai import OpenAI

from .embeds import PiEmbed
from .exceptions import OllamaAPIError

# CHATGPT API


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


# OLLAMA API


OLLAMA_URL = "http://ollama:11434"
OLLAMA_PARAMS = {"model": "phi3", "stream": False}


async def ask_ollama(prompt: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{OLLAMA_URL}/api/generate", json={**OLLAMA_PARAMS, "prompt": prompt}) as resp:
            if resp.status == 200:
                data = await resp.json()
            else:
                logging.error(f"Ollama API error: {resp}")
                raise OllamaAPIError

    embed = discord.Embed(
        title="Ask Me Anything",
        description=data["response"],
    )
    embed.set_footer(text=f"Prompt sent to phi3: {prompt}")

    return PiEmbed(embed=embed)
