import flask
import jinja2

class Sekazi():

    def init_app(app):
        ## Add extensions
        app.jinja_env.add_extension(ActiveCheckerExtension)

    def __init__(self, app=None):
        if app:
            self.init_app(app)


class AddToBlock(jinja2.ext.Extension):

    tags = set(['addtoblock'])

    def _render_tag(self, context, caller):
        return jinja2.Markup(self.template % unicode(context['active']))

    def parse(self, parser):
        context = jinja2.nodes.ContextReference()
        lineno = next(parser.stream).lineno
        node = self.call_method('_render_tag', [context], lineno=lineno)


class ActiveCheckerExtension(jinja2.ext.Extension):
    """
    This will give us a {% check_active %} tag.
    """

    template = 'Active is : %s'
    tags = set(['check_active'])

    def _render_tag(self, context, caller):
        return jinja2.Markup(self.template % unicode(context['active']))

    def parse(self, parser):
        ctx_ref = jinja2.nodes.ContextReference()
        lineno = next(parser.stream).lineno
        node = self.call_method('_render_tag', [ctx_ref], lineno=lineno)
