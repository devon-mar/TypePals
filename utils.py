import discord
import jinja2
import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random

from better_profanity import profanity
import textwrap


def render_template(template: str, **kwargs) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="templates/"), trim_blocks=True)
    template = env.get_template(template)
    return template.render(**kwargs)


def check_message(msg: str) -> bool:
    """
    Returns True if the message is appropriate.
    """
    if len(msg) > 400 or profanity.contains_profanity(msg):
        return False
    else:
        return True


def get_image(msg: str) -> discord.File:
    font_type = ImageFont.truetype("fonts/arial.ttf", 15)

    img = Image.open(f"backgrounds/{random.randint(0,2)}.jpg")
    width, height = img.size

    lines = textwrap.wrap(msg, width=50)

    draw = ImageDraw.Draw(img)

    for line in lines:
        draw.text((width / 10, height / 5), line, (0, 0, 0), font=font_type)
        height += 100

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return discord.File(bio, filename="reply.PNG")


def ceildiv(a, b):
    # https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
    return -(-a // b)
