from dotenv import load_dotenv
import discord
import os
import constants
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from models import Base, MessageRequest, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import render_template

DB_URI = os.getenv("DB_URI", default="sqlite:///:memory:")
engine = create_engine(DB_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=constants.COMMAND_PREFIX)


@bot.event
async def on_ready():
    bot.messages = []
    print(f"Logged in as {bot.user.name} {bot.user.id}")


@bot.command(name="ping",
             brief="Replies pong",
             description="Literally just replies pong")
async def ping(ctx):
    await ctx.reply("pong")


@bot.command(name=constants.GET_MSG_REQ_CMD,
             brief="Bot will send a message or request you can reply to",
             description="View others' messages and requests you can respond to.\nYou can respond"
                         "to them by right clicking the message and using Discord's own "
                         "\"Reply\" feature.")
async def get_msg(ctx):
    msg_req = (
        session.query(MessageRequest)
               .filter(MessageRequest.user_id != ctx.author.id)
               .filter(~MessageRequest.sent_messages.any(Response.user_id == ctx.author.id)).first()
    )
    if msg_req is None:
        await ctx.reply(constants.NO_MESSAGES)
    else:
        await msg_req.send(ctx.channel, session)


@bot.command(name=constants.RETRIEVE_MY_MSGS_CMD,
             brief="Bot sends you the responses sent to your message/request",
             description="The bot will send back the responses to each of your messages/requests.")
async def retrieve_my_msgs(ctx):
    my_mrs = session.query(MessageRequest).filter_by(user_id=ctx.author.id)
    if my_mrs.count() == 0:
        await ctx.channel.send(constants.NO_REQUESTS)
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
            await message.reply(constants.BAD_MESSAGE_REF)
        else:
            await rsp.set_message(message, session)
            await message.add_reaction(emoji=constants.SUCCESS_EMOJI)

    elif message.content.startswith(constants.COMMAND_PREFIX):
        await bot.process_commands(message)
    else:
        await MessageRequest.create(message.content, message.author.id, session)
        await message.add_reaction(emoji=constants.SUCCESS_EMOJI)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.reply(constants.INVALID_COMMAND)

bot.run(DISCORD_TOKEN)
