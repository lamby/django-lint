from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

from utils import is_model

class ModelFieldsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_fields'
    msgs = {
        'W6000': ('Nullable CharField', '',),
        'W6001': (
            'Naive tree structure implementation using ForeignKey(\'self\')',
        '',),
        'W6002': (
            'Too many fields; consider splitting model',
        '',),
    }

    def visit_class(self, node):
        self.field_count = 0

    def visit_callfunc(self, node):
        if not is_model(node.frame()):
            # We only care about fields attached to models
            return

        val = safe_infer(node)
        if not val or not val.root().name.startswith('django.db.models.fields'):
            # Not a field
            return

        self.field_count += 1
        if self.field_count == 30:
            self.add_message('W6002', node=node.frame())

        if val.name == 'ForeignKey':
            val = safe_infer(node.args[0])
            if val and val.value == 'self':
                self.add_message('W6001', node=node)

        # Check kwargs
        for arg in node.args:
            if not isinstance(arg, astng.Keyword):
                continue

            expr = safe_infer(arg.expr)
            if not expr:
                continue

            if val.name == 'CharField':
                if arg.name == 'null' and isinstance(expr, astng.Const) and expr.value is True:
                    self.add_message('W6000', node=node)
