from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class ModelFieldsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_fields'
    msgs = {
        'W6000': ('Nullable CharField', '',),
        'W6001': (
            'Naive tree structure implementation using ForeignKey(\'self\')',
        '',),
    }

    def visit_callfunc(self, node):
        val = safe_infer(node)
        if not val:
            return

        if not val.root().name.startswith('django.db.models.fields'):
            return

        if val.name == 'ForeignKey':
            val = safe_infer(node.args[0])
            if val and val.value == 'self':
                self.add_message('W6001', line=node.lineno)

        # Check kwargs
        for arg in node.args:
            if not isinstance(arg, astng.Keyword):
                continue

            expr = safe_infer(arg.expr)
            if not expr:
                continue

            if val.name == 'CharField' and arg.name == 'null' and \
                    isinstance(expr, astng.Const) and expr.value is True:
                self.add_message('W6000', line=node.lineno)
