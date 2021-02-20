from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
from models import MessageRequest


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
        # TODO: change this
        msg_req = bot.messages[0]
        await msg_req.send(ctx.channel)
    else:
        await ctx.channel.send("No messages!")


@bot.event
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.channel.DMChannel) or message.author.bot:
        return

    if message.reference is not None:
        # TODO: this is terrible
        for m in bot.messages:
            if m.reply_id == message.reference.message_id:
                m.replied = True
                user = await bot.fetch_user(m.user_id)
                await user.send(f"You got a reply from {message.author.name}: {message.content}")
                await message.channel.send("Sent your reply")
    elif message.content.startswith('/'):
        await bot.process_commands(message)
    else:
        bot.messages.append(MessageRequest(message.content, message.author.id))
        await message.channel.send("Received!")

bot.run(DISCORD_TOKEN)
