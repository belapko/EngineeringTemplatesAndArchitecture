import os.path

from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):
	env = Environment()
	env.loader = FileSystemLoader(folder)
	template = env.get_template(template_name)
	return template.render(**kwargs)
