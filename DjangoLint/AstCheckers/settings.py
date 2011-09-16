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

class SettingsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_settings_checker'
    msgs = {
        'W7001': ('Missing required field %r', '',),
        'W7002': ('Empty %r setting', '',),
        'W7003': ('%s after %s', ''),
        'W7005': ('Non-absolute directory %r in TEMPLATE_DIRS', ''),
        'W7006': ('%r in TEMPLATE_DIRS should use forward slashes', ''),
    }

    def leave_module(self, node):
        if node.name.split('.')[-1] != 'settings':
            return

        self.check_required_fields(node)
        self.check_middleware(node)
        self.check_template_dirs(node)

    def check_required_fields(self, node):
        REQUIRED_FIELDS = {
            'DEBUG': bool,
            'TEMPLATE_DEBUG': bool,
            'INSTALLED_APPS': tuple,
            'MANAGERS': tuple,
            'ADMINS': tuple,
            'MIDDLEWARE_CLASSES': tuple,
        }

        for field, req_type in REQUIRED_FIELDS.iteritems():
            if field not in node.locals.keys():
                self.add_message('W7001', args=field, node=node)
                continue

            if req_type is tuple:
                ass = node.locals[field][-1]
                val = safe_infer(ass)

                if val and not val.get_children():
                    self.add_message('W7002', args=field, node=ass)

    def get_constant_values(self, node, key):
        try:
            ass = node.locals[key][-1]
        except KeyError:
            return

        try:
            xs = safe_infer(ass).get_children()
        except AttributeError:
            return

        try:
            xs_iterable = iter(xs)
        except TypeError:
            return

        return [(x, x.value) for x in xs if isinstance(safe_infer(x), astng.Const)]

    def check_middleware(self, node):
        middleware = self.get_constant_values(node, 'MIDDLEWARE_CLASSES')
        if middleware is None:
            return

        relations = ((
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ), (
            'django.middleware.http.ConditionalGetMiddleware',
            'django.middleware.common.CommonMiddleware',
        ))

        lookup = [y for x, y in middleware]
        node_lookup = dict([(y, x) for x, y in middleware])

        for a, b in relations:
            try:
                if lookup.index(a) > lookup.index(b):
                    self.add_message(
                        'W7003',
                        args=tuple([x.split('.')[-1] for x in (a, b)]),
                        node=node_lookup[a],
                    )
            except ValueError:
                pass

    def check_template_dirs(self, node):
        template_dirs = self.get_constant_values(node, 'TEMPLATE_DIRS')
        if template_dirs is None:
            return

        for dirnode, dirname in template_dirs:
            if not (dirname.startswith('/') or dirname[1:].startswith(':')):
                self.add_message('W7005', args=dirname, node=dirnode)

            if dirname.find('\\') > 0:
                self.add_message('W7006', args=dirname, node=dirnode)
