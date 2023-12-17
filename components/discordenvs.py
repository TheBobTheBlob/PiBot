import os

import discord
from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX")

if (color := os.getenv("COLOR")) is not None:
    COLOR = discord.Color.from_str(color)
else:
    COLOR = discord.Color.blurple()
