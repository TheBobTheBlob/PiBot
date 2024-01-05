import os

import discord
from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX")

if (color := os.getenv("COLOR")) is not None:
    COLOR = discord.Color.from_str(color)
else:
    COLOR = discord.Color.blurple()


class PiEmbed:
    def __init__(self, embed, view: None | discord.ui.View = None, file: None | discord.File = None):
        self.embed = embed
        self.view = view
        self.file = file
