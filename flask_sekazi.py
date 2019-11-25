import flask
import jinja2
from jinja2 import nodes
from jinja2.ext import Extension
import collections

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

class Sekazi():

    def init_app(self, app):
        ## Add extensions
        app.jinja_env.add_extension(AddToBlock)
        app.jinja_env.add_extension(RenderBlock)
        app.jinja_env.sekazi_tags = dict()

    def __init__(self, app=None):
        if app:
            self.init_app(app)

class AddToBlock(Extension):

    tags = set(['addtoblock'])

    def _render_tag(self, name, caller):
        context = self.environment.sekazi_tags
        blocks = context.get(name)
        if blocks is None:
            blocks = OrderedSet()
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
        return jinja2.Markup('\n'.join(reversed( context.get(name, []) ) ))

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()
        args = [name]

        return nodes.CallBlock(self.call_method('_render_tag', args),
                               [], [], []).set_lineno(lineno)

