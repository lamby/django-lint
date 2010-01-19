# -*- coding: utf-8 -*-

# django-lint -- Static analysis tool for Django projects and applications
# Copyright (C) 2008-2009 Chris Lamb <chris@chris-lamb.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

from utils import is_model

class ModelFieldsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_fields'
    msgs = {
        'W6000': ('%s: Nullable CharField or TextField', ''),
        'W6001': (
            "%s: Naive tree structure implementation using ForeignKey('self')",
        ''),
        'W6002': (
            'Model has too many fields (%d/%d); consider splitting model',
        ''),
        'W6003': ('Model has no fields', ''),
        'W6004': ('%s: Field is nullable but blank=False', ''),
        'W6005': ('%s: uses brittle unique_for_%s', ''),
        'W6006': ('%s: ForeignKey missing related_name', ''),
        'W6007': (
            '%s: CharField with huge (%d/%d) max_length instead of TextField',
        ''),
        'W6008': ('%s: Uses superceded auto_now or auto_now_add', ''),
        'W6009': (
            '%s: NullBooleanField instead of BooleanField with null=True',
        ''),
        'W6010': ('%s: %s has database-dependent limits', ''),
        'W6011': ('%s: URLField uses verify_exists=True default', ''),
        'W6012': (
            '%s: BooleanField with default=True will not be reflected in database',
        ''),
        'W6013': (
            '%s: Unique ForeignKey constraint better modelled as OneToOneField',
        ''),
        'W6014': ('%s: primary_key=True should imply unique=True', ''),
        'W6015': ('%s: %s=False is implicit', ''),
        'W6016': ('%s: Nullable ManyToManyField makes no sense', ''),
    }

    options = (
        ('max-model-fields', {
            'default': 20,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum number of fields for a model',
        }),
        ('max-charfield-length', {
            'default': 512,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum size of max_length on a CharField',
        }),
    )

    def visit_module(self, node):
        self.field_count = 0

    def leave_class(self, node):
        if not is_model(node):
            return

        if is_model(node, check_base_classes=False) and self.field_count == 0:
            self.add_message('W6003', node=node)
        elif self.field_count > self.config.max_model_fields:
            self.add_message('W6002', node=node,
                args=(self.field_count, self.config.max_model_fields))

        self.field_count = 0

    def visit_callfunc(self, node):
        if not is_model(node.frame()):
            # We only care about fields attached to models
            return

        val = safe_infer(node)
        if not val or not val.root().name.startswith('django.db.models.fields'):
            # Not a field
            return

        assname = '(unknown name)'
        x = node.parent.get_children().next()
        if isinstance(x, astng.AssName):
            assname = x.name

        self.field_count += 1

        # Parse kwargs
        options = dict([(option, None) for option in (
            'null',
            'blank',
            'unique',
            'default',
            'auto_now',
            'primary_key',
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

            for option in options.keys():
                if arg.arg == option:
                    try:
                        options[option] = safe_infer(arg.value).value
                    except AttributeError:
                        # Don't lint this field if we cannot infer everything
                        return

        if not val.name.lower().startswith('null'):
            for option in ('null', 'blank'):
                if options[option] is False:
                    self.add_message('W6015', node=node, args=(assname, option,))

        # Field type specific checks
        if val.name in ('CharField', 'TextField'):
            if options['null']:
                self.add_message('W6000', node=node, args=(assname,))

            if val.name == 'CharField' and \
                    options['max_length'] > self.config.max_charfield_length:
                self.add_message('W6007', node=node, args=(
                    assname,
                    options['max_length'],
                    self.config.max_charfield_length,
                ))

        elif val.name == 'BooleanField':
            if options['default']:
                self.add_message('W6012', node=node, args=(assname,))

        elif val.name == 'ForeignKey':
            val = safe_infer(node.args[0])
            if isinstance(val, astng.Const) and val.value == 'self':
                self.add_message('W6001', node=node, args=(assname,))

            elif not options['related_name']:
                self.add_message('W6006', node=node, args=(assname,))

            if options['primary_key'] and options['unique'] is False:
                self.add_message('W6014', node=node, args=(assname,))
            elif options['primary_key'] or options['unique']:
                self.add_message('W6013', node=node, args=(assname,))

        elif val.name == 'URLField':
            if options['verify_exists'] is None:
                self.add_message('W6011', node=node, args=(assname,))

        elif val.name in ('PositiveSmallIntegerField', 'SmallIntegerField'):
            self.add_message('W6010', node=node, args=(assname, val.name))

        elif val.name == 'NullBooleanField':
            self.add_message('W6009', node=node, args=(assname,))

        elif val.name == 'ManyToManyField':
            if options['null']:
                self.add_message('W6016', node=node, args=(assname,))

        # Generic checks
        if options['null'] and not options['blank']:
            self.add_message('W6004', node=node, args=(assname,))

        if options['auto_now'] or options['auto_now_add']:
            self.add_message('W6008', node=node, args=(assname,))

        for suffix in ('date', 'month', 'year'):
            if options['unique_for_%s' % suffix]:
                self.add_message('W6005', node=node, args=(assname, suffix))
