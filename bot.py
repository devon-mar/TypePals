from dotenv import load_dotenv
import discord
import os
import constants
from discord.ext import commands
from discord.ext.commands import CommandNotFound, Context
from models import Base, MessageRequest, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import render_template, check_message, get_image, ceildiv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DELETE_THRESHOLD = int(os.getenv("DELETE_THRESHOLD", 0))
DATABASE_URL = os.getenv("DATABASE_URL", default="sqlite:///:memory:")
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

help_command = commands.DefaultHelpCommand(
    no_category='Commands'
)


bot = commands.Bot(command_prefix=constants.COMMAND_PREFIX, help_command=help_command)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} {bot.user.id}")


@bot.command(
    name="ping",
    brief="Replies pong",
    description="Literally just replies pong"
)
async def ping(ctx: Context):
    await ctx.reply("pong")


@bot.command(
    name=constants.GET_MSG_REQ_CMD,
    brief="Bot will send a message or request you can reply to",
    description="View others' messages and requests you can respond to.\nYou can respond"
    "to them by right clicking the message and using Discord's own "
    "\"Reply\" feature."
)
async def get_msg(ctx: Context):
    msg_req = (
        session.query(MessageRequest)
               .filter(MessageRequest.user_id != ctx.author.id)
               .filter(~MessageRequest.responses.any(Response.user_id == ctx.author.id)).first()
    )
    if msg_req is None:
        await ctx.reply(constants.NO_MESSAGES)
    else:
        await msg_req.send(ctx.channel, session)


@bot.command(
    name=constants.RETRIEVE_MY_MSGS_CMD,
    brief="Bot retrieves the responses sent to your message/request",
    description="The bot will send back the responses to each of your messages/requests."
)
async def retrieve_my_msgs(ctx: Context, as_images: str = ""):
    my_mrs = session.query(MessageRequest).filter_by(user_id=ctx.author.id)
    if my_mrs.count() == 0:
        await ctx.send(constants.NO_REQUESTS)
    for req in my_mrs:
        mc = req.responses.count()
        if mc == 0:
            await ctx.send(render_template("no_replies.j2", req=req))
        elif as_images == "images":
            files = [get_image(r.message) for r in req.responses]
            page_count = ceildiv(len(files), 10)
            for i in range(page_count):
                await ctx.send(
                    render_template("read_replies_img.j2", req=req, i=i, pc=page_count),
                    files=files[i * 10:i * 10 + 10]
                )
        else:
            await ctx.channel.send(render_template("read_replies.j2", req=req, mc=mc))
            if mc > DELETE_THRESHOLD:
                req.delete(session)


@bot.event
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.channel.DMChannel) or message.author.bot:
        return

    if message.reference is not None:
        if not check_message(message.content):
            await message.reply(constants.REJECT_MESSAGE)
            return
        rsp = session.query(Response).filter_by(discord_message=message.reference.message_id).first()
        if rsp is None:
            print(f"Ref not in DB: {message.reference.message_id}")
            await message.reply(constants.BAD_MESSAGE_REF)
        else:
            rsp.set_message(message, session)
            await message.add_reaction(emoji=constants.SUCCESS_EMOJI)
    elif message.content.startswith(constants.COMMAND_PREFIX):
        await bot.process_commands(message)
    else:
        if check_message(message.content):
            MessageRequest.create(message.content, message.author.id, session)
            await message.add_reaction(emoji=constants.SUCCESS_EMOJI)
        else:
            await message.reply(constants.REJECT_MESSAGE)


@bot.event
async def on_command_error(ctx: Context, error: Exception):
    if isinstance(error, CommandNotFound):
        await ctx.reply(constants.INVALID_COMMAND)

bot.run(DISCORD_TOKEN)
