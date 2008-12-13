from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class SizeChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_size_checker'
    msgs = {
        'W8001': (
            '%r is actually a directory; consider splitting application',
        '',),
    }

    def leave_module(self, node):
        for candidate in ('views', 'models'):
            if not node.name.endswith('.%s' % candidate):
                continue

            if node.file.endswith('__init__.py'):
                self.add_message('W8001', args=node.name, node=node)
