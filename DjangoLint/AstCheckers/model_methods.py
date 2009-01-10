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
            'Too many models (%d/%d); consider splitting application',
        '',),
        'W8011': ('Use __unicode__ instead of __str__', '',),
        'W8012': ('Method should come after standard model methods', '',),
        'W8013': ('Standard model method should come before %r', '',),
        'W8014': ('Missing __unicode__ method', '',),
    }

    options = (
        ('max-models', {
            'default': 15,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum number of models per module',
        }),
    )

    def visit_module(self, node):
        self.model_count = 0

    def leave_module(self, node):
        if self.model_count >= self.config.max_models:
            self.add_message('W8010', node=node.root(),
                args=(self.model_count, self.config.max_models))

    def visit_function(self, node):
        if not is_model(node.parent.frame()):
            return

        if node.name == '__str__':
            self.add_message('W8011', node=node)

        try:
            idx = [
                '__unicode__',
                '__str__',
                'save',
                'get_absolute_url',
            ].index(node.name)

            if self.prev_idx == -1:
                self.add_message('W8012', node=self.prev_node)

            elif idx < self.prev_idx:
                self.add_message('W8013', node=node, args=self.prev_node.name)

        except ValueError:
            idx = -1

        self.prev_idx = idx
        self.prev_node = node

    def visit_class(self, node):
        if not is_model(node):
            return

        if '__unicode__' not in [x.name for x in node.mymethods()]:
            self.add_message('W8014', node=node)

        self.model_count += 1
        self.prev_idx = None
        self.prev_name = None
