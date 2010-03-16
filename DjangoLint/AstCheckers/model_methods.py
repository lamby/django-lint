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

import os.path

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

from utils import is_model

try:
    from itertools import combinations
except ImportError:
    # Python <= 2.5 fallback
    def combinations(iterable, r):
        if r:
            for i, cur in enumerate(iterable):
                for xs in combinations(iterable[:i] + iterable[i + 1:], r - 1):
                    yield [cur] + xs
        else:
            yield []

class ModelMethodsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_model_models'
    msgs = {
        'W8010': (
            'Too many models (%d/%d); consider splitting application',
        '',),
        'W8011': ('Use __unicode__ instead of __str__', '',),
        'W8012': ('Method should come after standard model methods', '',),
        'W8013': ('%s should come before %r', '',),
        'W8015': (
            '%d models have common prefix (%r) - rename or split application',
        '',),
    }

    options = (
        ('max-models', {
            'default': 10,
            'type': 'int',
            'metavar': '<int>',
            'help': 'Maximum number of models per module',
        }),
    )

    def visit_module(self, node):
        self.model_names = []

    def leave_module(self, node):
        if len(self.model_names) >= self.config.max_models:
            self.add_message('W8010', node=node.root(),
                args=(len(self.model_names), self.config.max_models))

        if not self.model_names:
            return

        for names in combinations(self.model_names, 4):
            common = os.path.commonprefix(names)
            if len(common) >= 4:
                # Whitelist a few common names
                if common.lower() in ('abstract',):
                    continue

                # How many actually have this prefix?
                xs = filter(lambda x: x.startswith(common), self.model_names)

                self.add_message('W8015', node=node.root(),
                    args=(len(xs), common,))
                break

    def _visit_django_attribute(self, node, is_method=True):
        try:
            idx = [
                'Meta',
                '__unicode__',
                '__str__',
                'save',
                'delete',
                'get_absolute_url',
            ].index(node.name)

            if self.prev_idx == -1:
                self.add_message('W8012', node=self.prev_node)

            elif idx < self.prev_idx:
                noun = is_method and 'Standard model method' or '"Meta" class'
                self.add_message(
                    'W8013', node=node, args=(noun, self.prev_node.name)
                )

        except ValueError:
            idx = -1

        self.prev_idx = idx
        self.prev_node = node

    def visit_function(self, node):
        if not is_model(node.parent.frame()):
            return

        if node.name == '__str__':
            self.add_message('W8011', node=node)

        self._visit_django_attribute(node)

    def visit_class(self, node):
        if is_model(node):
            self.model_names.append(node.name)
            self.prev_idx = None
            self.prev_node = None

        elif is_model(node.parent.frame()):
            # Nested class
            self._visit_django_attribute(node, is_method=False)

    def visit_assname(self, node):
        if not is_model(node.parent.frame()):
            return

        if self.prev_idx >= 0:
            self.add_message('W8013', node=node, args=(
                '%r assignment' % node.name, self.prev_node.name,
            ))

    def leave_class(self, node):
        if node.name == 'Meta' and is_model(node.parent.parent):
            # Annotate the model with information from the Meta class
            try:
                val = safe_infer(node.locals['abstract'][-1]).value
                if val is True:
                    node.parent.parent._django_abstract = True
            except KeyError:
                pass
            return

        if not is_model(node):
            return
