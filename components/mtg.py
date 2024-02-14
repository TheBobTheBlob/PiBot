import re

import aiohttp
import discord

from .discordenvs import PREFIX, PiEmbed, PiList

URL = "https://api.scryfall.com/"


async def card_brackets(message: str) -> PiList:
    cards = re.findall(r"\[\[(.+?)\]\]", message)
    embeds = PiList()

    for card in cards:
        embeds.add(await get_card(card))

    return embeds


async def card_cmd(message: str) -> PiEmbed:
    card = message.lstrip(f"{PREFIX}card")
    embed = await get_card(card)

    return embed


async def card_slash(name: str) -> PiEmbed:
    embed = await get_card(name)
    return embed


# API call to get card image
async def get_card(name: str) -> PiEmbed:
    params = {"q": name, "format": "json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(URL + "cards/search/", params=params) as resp:
            matches = await resp.json()

    view = None

    if matches["object"] == "error":
        embed = discord.Embed(title=f'No cards found for "{name}"')
    else:
        if matches["total_cards"] == 1:
            embed = card_image_embed(matches["data"][0])
        elif matches["total_cards"] <= 5:  # 5 is the maximum number of buttons per Discord message
            embed = discord.Embed(
                title=f'Multiple cards found for "{name}"',
                description="The following cards all match your search term. Select one to view.",
            )

            view = discord.ui.View()
            for card in matches["data"]:
                view.add_item(item=MultiCardButton(card))
        else:
            embed = discord.Embed(
                title=f'Multiple cards found for "{name}"',
                description="More than 5 cards match your search. Please refine your search term.",
            )

    return PiEmbed(embed=embed, view=view)


# Class for dynamic buttons
class MultiCardButton(discord.ui.Button):
    def __init__(self, data):
        self.data = data
        super().__init__(style=discord.ButtonStyle.grey, label=self.data["name"])

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = card_image_embed(self.data)
        await interaction.response.edit_message(embed=embed, view=None)


# Creates embed with title and image
def card_image_embed(data) -> discord.Embed:
    embed = discord.Embed(title=data["name"], url=data["scryfall_uri"])

    def get_image_url(urls: dict) -> str | None:
        if "png" in urls:
            return urls["png"]
        elif "large" in urls:
            return urls["large"]
        elif "normal" in urls:
            return urls["normal"]
        else:
            return None

    if "card_faces" in data and "image_uris" not in data:
        embed.set_image(url=get_image_url(data["card_faces"][0]["image_uris"]))
        embed.set_thumbnail(url=get_image_url(data["card_faces"][1]["image_uris"]))
    else:
        embed.set_image(url=get_image_url(data["image_uris"]))

    return embed
