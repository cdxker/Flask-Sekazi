import flask
import jinja2
from jinja2 import nodes
from jinja2.ext import Extension
from cachelib import SimpleCache

class Sekazi():

    def init_app(self, app):
        ## Add extensions
        app.jinja_env.add_extension(AddToBlock)
        app.jinja_env.add_extension(RenderBlock)
        app.jinja_env.add_extension(FragmentCacheExtension)
        app.jinja_env.fragment_cache = SimpleCache()
        app.jinja_env.sekazi_tags = {}

    def __init__(self, app=None):
        if app:
            self.init_app(app)


class AddToBlock(Extension):

    tags = set(['addtoblock'])

    def _render_tag(self, name, caller):
        print("hi")
        context = self.environment.sekazi_tags
        blocks = context.get(name)
        if blocks is None:
            blocks = set()
        blocks.add( caller() )
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
        body = parser.parse_statements(['name:endrenderblock'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_render_tag', args),
                               [], [], body).set_lineno(lineno)

class FragmentCacheExtension(Extension):
    # a set of names that trigger the extension.
    tags = {'cache'}

    def __init__(self, environment):
        super(FragmentCacheExtension, self).__init__(environment)

        # add the defaults to the environment
        environment.extend(
            fragment_cache_prefix='',
            fragment_cache=None
        )

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        if parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))
        body = parser.parse_statements(['name:endcache'], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(self.call_method('_cache_support', args),
                               [], [], body).set_lineno(lineno)

    def _cache_support(self, name, timeout, caller):
        """Helper callback."""
        key = self.environment.fragment_cache_prefix + name

        rv = self.environment.fragment_cache.get(key)
        if rv is not None:
            return rv
        rv = caller()
        self.environment.fragment_cache.add(key, rv, timeout)
        return rv
