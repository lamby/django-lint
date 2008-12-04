from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

class DjangoLintASTNGChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_lint'
    msgs = {
        'W6000': ('Nullable CharField', '',),
    }

    options = ()
    priority = -1

    def visit_callfunc(self, node):
        if not node.node.attrname == 'CharField':
            return

        for arg in node.args:
            if not isinstance(arg, astng.Keyword) or arg.name != 'null':
                continue

            if not isinstance(arg.expr, astng.Name) or arg.expr.name != 'True':
                continue

            self.add_message('W6000', line=node.lineno)

def register(linter):
    linter.register_checker(DjangoLintASTNGChecker(linter))
