from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class SettingsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_settings_checker'
    msgs = {
        'W7001': ('Missing required field %r', '',),
        'W7002': ('Empty %r setting', '',),
    }

    def leave_module(self, node):
        if node.name.split('.')[-1] != 'settings':
            return

        REQUIRED_FIELDS = {
            'DEBUG': bool,
            'TEMPLATE_DEBUG': bool,
            'INSTALLED_APPS': tuple,
            'MANAGERS': tuple,
            'ADMINS': tuple,
        }

        for field, req_type in REQUIRED_FIELDS.iteritems():
            if field not in node.locals.keys():
                self.add_message('W7001', args=field, node=node)
                continue

            if req_type is tuple:
                ass = node.locals[field][-1]
                val = safe_infer(ass)

                if val and not val.nodes:
                    self.add_message('W7002', args=field, node=ass)
