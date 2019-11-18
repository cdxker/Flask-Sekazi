import flask
import jinja2
from jinja2 import nodes
from jinja2.ext import Extension

class Sekazi():

    def init_app(self, app):
        ## Add extensions
        app.jinja_env.add_extension(AddToBlock)
        app.jinja_env.add_extension(RenderBlock)
        app.jinja_env.sekazi_tags = {}

    def __init__(self, app=None):
        if app:
            self.init_app(app)

class AddToBlock(Extension):

    tags = set(['addtoblock'])

    def _render_tag(self, name, caller):
        context = self.environment.sekazi_tags
        blocks = context.get(name)
        if blocks is None:
            blocks = set()
        blocks.add( caller().strip() )
        context[name] = blocks
        return jinja2.Markup("")

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        name = parser.parse_expression()

        body = parser.parse_statements(['name:endaddtoblock'], drop_needle=True)
        args = [name]

        return nodes.CallBlock(self.call_method('_render_tag', args),
                               [], [], body).set_lineno(lineno)

class RenderBlock(Extension):

    tags = set(['renderblock'])

    def _render_tag(self, name: str, caller):
        context = self.environment.sekazi_tags
        return jinja2.Markup('\n'.join(context.get(name, [])))

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()
        args = [name]

        return nodes.CallBlock(self.call_method('_render_tag', args),
                               [], [], []).set_lineno(lineno)

