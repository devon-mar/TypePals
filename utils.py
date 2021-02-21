import jinja2


async def render_template(template: str, **kwargs) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="templates/"), trim_blocks=True)
    template = env.get_template(template)
    return template.render(**kwargs)
