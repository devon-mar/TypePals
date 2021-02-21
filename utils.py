import jinja2
from better_profanity import profanity


def render_template(template: str, **kwargs) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="templates/"), trim_blocks=True)
    template = env.get_template(template)
    return template.render(**kwargs)


def check_message(msg: str) -> bool:
    """
    Returns True if the message is appropriate.
    """
    if (profanity.contains_profanity(msg)) or (len(msg) > 400):
        return False
    else:
        return True

