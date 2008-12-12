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
        'W8002': (
            'Too many models; consider splitting application',
        '',),
    }

    def visit_module(self, node):
        self.model_count = 0

    def leave_module(self, node):
        for candidate in ('views', 'models'):
            if not node.name.endswith('.%s' % candidate):
                continue

            if node.file.endswith('__init__.py'):
                self.add_message('W8001', args=node.name)

    def leave_class(self, node):
        for b in node.bases:
            val = safe_infer(b)
            if not val:
                continue

            if "%s.%s" % (val.root().name, val.name) == 'django.db.models.base.Model':
                self.model_count += 1
                if self.model_count == 10:
                    self.add_message('W8002')
