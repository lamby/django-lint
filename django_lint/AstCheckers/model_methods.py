from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class ModelMethodsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_models'
    msgs = {
        'W8010': (
            'Too many models; consider splitting application',
        '',),
    }

    def visit_module(self, node):
        self.model_count = 0

    def leave_class(self, node):
        for b in node.bases:
            val = safe_infer(b)
            if not val:
                continue

            if "%s.%s" % (val.root().name, val.name) == 'django.db.models.base.Model':
                self.model_count += 1
                if self.model_count == 10:
                    self.add_message('W8010')
