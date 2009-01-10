from logilab import astng

from pylint.checkers.utils import safe_infer

def is_model(node):
    if not isinstance(node, astng.Class):
        return False

    for base in node.bases:
        val = safe_infer(base)
        if not val:
            continue

        if "%s.%s" % (val.root().name, val.name) == 'django.db.models.base.Model':
            return True

    return False
