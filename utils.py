import discord
import jinja2
import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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


def get_image(background: str, msg: str) -> discord.File:

    font_type = ImageFont.truetype("Font/arial.ttf", 15)

    img = Image.open("backgrounds.1.jpg")
    WIDTH , HEIGHT = img.size

    lines = textwrap.wrap(msg, width=50)

    draw = ImageDraw.Draw(img)

    for line in lines:
        width = height = font_type.getsize(line)
        draw.text((WIDTH / 10, HEIGHT / 5), msg, (0, 0, 0), font=font_type)
        HEIGHT += 100


    img = Image.open(f"backgrounds/{background}")
    bio = io.BytesIO()
    img.save(bio, format="PNG", filename="reply.PNG")
    bio.seek(0)
    return discord.File(bio)
