import os
import discord
from discord.ext import commands
import time

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Valorant"))
    print("ok")
