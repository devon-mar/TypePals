from dotenv import load_dotenv
import discord
import os
import random
from discord.ext import commands


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    bot.messages = []
    print(f"Logged in as {bot.user.name} {bot.user.id}")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command(name="get_msg")
async def get_msg(ctx):
    if len(bot.messages) > 0:
        await ctx.channel.send(bot.messages.pop())
    else:
        await ctx.channel.send("No messages!")


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.channel.DMChannel) and not message.author.bot:
        if message.content.startswith('/'):
            await bot.process_commands(message)
        else:
            bot.messages.append(message.content)
            await message.channel.send("Received!")

bot.run(DISCORD_TOKEN)
