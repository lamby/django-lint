from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

from utils import is_model

class ModelFieldsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_fields'
    msgs = {
        'W6000': ('Nullable CharField or TextField', ''),
        'W6001': (
            "Naive tree structure implementation using ForeignKey('self')",
        ''),
        'W6002': (
            'Model has too many fields (%d/%d); consider splitting model',
        ''),
        'W6003': ('Model has no fields', ''),
        'W6004': ('Field is nullable but blank=False', ''),
        'W6005': ('Field uses brittle unique_for_%s', ''),
        'W6006': ('ForeignKey field missing related_name', ''),
        'W6007': (
            'Use TextField instead of CharField with huge (%d/%d) max_length',
        ''),
        'W6008': (
            'Date-related field uses brittle auto_now or auto_now_add',
        ''),
        'W6009': (
            'Use NullBooleanField instead of BooleanField with null=True',
        ''),
        'W6010': ('%s field has database-dependent limits', ''),
        'W6011': ('URLField uses verify_exists=True default', ''),
    }

    options = (
        ('max-model-fields', {
            'default': 30,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum number of fields for a model',
        }),
        ('max-charfield-length', {
            'default': 500,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum size of max_length on a CharField',
        }),
    )


    def visit_class(self, node):
        self.field_count = 0

    def leave_class(self, node):
        if not is_model(node):
            return

        if self.field_count == 0:
            self.add_message('W6003', node=node)
        elif self.field_count >= self.config.max_model_fields:
            self.add_message('W6002', node=node,
                args=(self.field_count, self.config.max_model_fields))

    def visit_callfunc(self, node):
        if not is_model(node.frame()):
            # We only care about fields attached to models
            return

        val = safe_infer(node)
        if not val or not val.root().name.startswith('django.db.models.fields'):
            # Not a field
            return

        self.field_count += 1

        # Prase kwargs
        options = dict([(option, False) for option in (
            'null',
            'blank',
            'auto_now',
            'auto_now_add',
            'verify_exists',
            'related_name',
            'max_length',
            'unique_for_date',
            'unique_for_month',
            'unique_for_year',
        )])

        for arg in node.args:
            if not isinstance(arg, astng.Keyword):
                continue

            expr = safe_infer(arg.expr)
            if not expr or not isinstance(expr, astng.Const):
                continue

            for option in options.keys():
                if arg.name == option:
                    options[option] = expr.value

        # Field type specific checks
        if val.name in ('CharField', 'TextField'):
            if options['null']:
                self.add_message('W6000', node=node)

            if val.name == 'CharField' and \
                    options['max_length'] >= self.config.max_charfield_length:
                self.add_message('W6007', node=node, args=(options['max_length'],
                    self.config.max_charfield_length))

        elif val.name == 'BooleanField' and options['null']:
            self.add_message('W6009', node=node)

        elif val.name == 'ForeignKey':
            val = safe_infer(node.args[0])
            if isinstance(val, astng.Const) and val.value == 'self':
                self.add_message('W6001', node=node)

            elif not options['related_name']:
                self.add_message('W6006', node=node)

        elif val.name == 'URLField':
            if options['verify_exists'] is not None:
                self.add_message('W6011', node=node)

        elif val.name in ('PositiveSmallIntegerField', 'SmallIntegerField'):
            self.add_message('W6010', node=node, args=val.name)


        # Generic checks
        if options['null'] and not options['blank']:
            self.add_message('W6004', node=node)

        if options['auto_now'] or options['auto_now_add']:
            self.add_message('W6008', node=node)

        for suffix in ('date', 'month', 'year'):
            if options['unique_for_%s' % suffix]:
                self.add_message('W6005', node=node, args=suffix)
