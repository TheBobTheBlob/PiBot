import re

import aiohttp
import discord

from .discordenvs import COLOR, PREFIX

URL = "https://api.scryfall.com/"


async def card_brackets(message: str) -> list:
    cards = re.findall(r"\[\[(.+?)\]\]", message)
    embeds = []

    for card in cards:
        embeds.append(await get_card_image(card))

    return embeds


async def card_cmd(message: str) -> list:
    card = message.lstrip(f"{PREFIX}card ")
    embed = await get_card_image(card)

    return [embed]


async def card_slash(name: str) -> list:
    embed = await get_card_image(name)

    return [embed]


# API call to get card image
async def get_card_image(name: str) -> dict:
    params = {"q": name, "format": "json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(URL + "cards/search/", params=params) as resp:
            matches = await resp.json()

    view = None

    if matches["object"] == "error":
        embed = discord.Embed(
            title=f'No cards found for "{name}"',
            color=COLOR,
        )
    else:
        if matches["total_cards"] == 1:
            embed = card_image_embed(matches["data"][0])

        elif matches["total_cards"] <= 5:
            embed = discord.Embed(
                title=f'Multiple cards found for "{name}"',
                description="The following cards all match your search term. Select one to view.",
                color=COLOR,
            )

            view = discord.ui.View()
            for card in matches["data"]:
                view.add_item(item=MultiCardButton(card))
        else:
            embed = discord.Embed(
                title=f'Multiple cards found for "{name}"',
                description="More than 5 cards match your search. Please refine your search term.",
                color=COLOR,
            )

    return {"embed": embed, "view": view}


# Class for dynamic buttons
class MultiCardButton(discord.ui.Button):
    def __init__(self, data):
        self.data = data
        super().__init__(style=discord.ButtonStyle.grey, label=self.data["name"])

    async def callback(self, interaction: discord.Interaction):
        embed = card_image_embed(self.data)
        await interaction.response.edit_message(embed=embed, view=None)


# Creates embed with title and image
def card_image_embed(data) -> discord.Embed:
    embed = discord.Embed(title=data["name"], url=data["scryfall_uri"], color=COLOR)

    def get_image_url(urls: dict) -> str | None:
        if "png" in urls:
            return urls["png"]
        elif "large" in urls:
            return urls["large"]
        else:
            return None

    if "card_faces" in data:
        embed.set_image(url=get_image_url(data["card_faces"][0]["image_uris"]))
        embed.set_thumbnail(url=get_image_url(data["card_faces"][1]["image_uris"]))
    else:
        embed.set_image(url=get_image_url(data["image_uris"]))

    return embed
