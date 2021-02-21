from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
from models import Base, MessageRequest, Response
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from utils import render_template

engine = create_engine("sqlite:///:memory:", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


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


@bot.command(name="get")
async def get_msg(ctx):
    req_count = session.query(MessageRequest).count()
    if req_count > 0:
        req = session.query(MessageRequest).first()
        await req.send(ctx.channel, session)
    else:
        await ctx.channel.send("No messages!")


@bot.command(name="read")
async def retrieve_my_msgs(ctx):
    my_mrs = session.query(MessageRequest).filter_by(user_id=ctx.author.id)
    if my_mrs.count() == 0:
        await ctx.channel.send(await render_template("no_requests.j2"))
    for req in my_mrs:
        mc = req.sent_messages.count()
        if mc == 0:
            await ctx.channel.send(await render_template("no_replies.j2", req=req))
        else:
            await ctx.channel.send(await render_template("read_replies.j2", req=req, mc=mc))
            req.delete(session)


@bot.event
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.channel.DMChannel) or message.author.bot:
        return

    if message.reference is not None:
        rsp = session.query(Response).filter_by(discord_message=message.reference.message_id).first()
        if rsp is None:
            print(f"Ref not in DB: {message.reference.message_id}")
        else:
            await rsp.set_message(message.content, session)
            await message.channel.send("Your replied has been received!")

    elif message.content.startswith('/'):
        await bot.process_commands(message)
    else:
        await MessageRequest.create(message.content, message.author.id, session)
        await message.channel.send("Received!")

bot.run(DISCORD_TOKEN)
