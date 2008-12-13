from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

from utils import is_model

class ModelMethodsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_models'
    msgs = {
        'W8010': (
            'Too many models; consider splitting application',
        '',),
        'W8011': ('Use __unicode__ instead of __str__', '',),
    }

    def visit_module(self, node):
        self.model_count = 0

    def leave_module(self, node):
        if self.model_count >= 10:
            self.add_message('W8010', node=node.root())

    def visit_class(self, node):
        if not is_model(node):
            return

        self.model_count += 1

        if '__str__' in node.locals:
            self.add_message('W8011', node=node.locals['__str__'][0])
