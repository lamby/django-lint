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

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

class SizeChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_size_checker'
    msgs = {
        'W8001': (
            '%r is actually a directory; consider splitting application',
        '',),
    }

    def leave_module(self, node):
        for candidate in ('views', 'models'):
            if not node.name.endswith('.%s' % candidate):
                continue

            if node.file.endswith('__init__.py'):
                # When 'models' is a directory, django.test.simple.run_tests
                # cannot tell the difference between a tests.py module that is
                # raising an ImportError and when it doesn't exist (so it
                # silently discards that app). This is not good!
                self.add_message('W8001', args=node.name, node=node)
