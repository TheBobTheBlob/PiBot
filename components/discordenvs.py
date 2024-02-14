import os

import discord
from dotenv import load_dotenv

load_dotenv()


PREFIX = os.environ["PREFIX"]
try:
    COLOR = discord.Color.from_str(os.environ["COLOR"])
except KeyError:
    COLOR = discord.Color.blurple()


class PiEmbed:
    def __init__(self, embed, view: None | discord.ui.View = None, file: None | discord.File = None):
        self.embed = embed
        self.view = view
        self.file = file

        self.embed.color = COLOR


class PiList:
    def __init__(self, embed: PiEmbed | None = None):
        self.list = [embed] if embed else []

    def add(self, embed: PiEmbed):
        self.list.append(embed)

    def remove(self, index: int):
        self.list.pop(index)

    def get(self, index: int) -> PiEmbed:
        if len(self.list) == 0:
            raise IndexError("No embeds")

        return self.list[index]

    def get_all(self) -> list[PiEmbed]:
        return self.list
