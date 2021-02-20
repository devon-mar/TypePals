from dotenv import load_dotenv
import discord
import os
import random
from discord.ext import commands


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MESSAGES = [
    "test1",
    "test2",
    "test3"
]

bot = commands.Bot(command_prefix="/")


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command()
async def get_msg(ctx):
    await ctx.channel.send(random.choice(MESSAGES))

bot.run(DISCORD_TOKEN)
