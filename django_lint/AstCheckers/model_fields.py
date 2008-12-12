from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class ModelFieldsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_fields'
    msgs = {
        'W6000': ('Nullable CharField', '',),
    }

    def visit_callfunc(self, node):
        val = safe_infer(node)
        if not val:
            return

        full_name = "%s.%s" % (val.root().name, val.name)
        if full_name != 'django.db.models.fields.CharField':
            return

        for arg in node.args:
            if not isinstance(arg, astng.Keyword) or arg.name != 'null':
                continue

            expr = safe_infer(arg.expr)
            if not expr:
                continue

            if isinstance(expr, astng.Const) and expr.value:
                self.add_message('W6000', line=node.lineno)
