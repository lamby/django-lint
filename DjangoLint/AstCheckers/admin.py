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

from .utils import nodeisinstance

class AdminChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_admin'
    msgs = {
        'W8020': (
            'Admin class %r not in admin.py',
            'loldongs',),
    }

    ADMIN_BASE_CLASSES = (
        'django.contrib.admin.options.ModelAdmin',
    )

    def visit_module(self, node):
        self.module = node

    def leave_class(self, node):
        if not nodeisinstance(node, self.ADMIN_BASE_CLASSES):
            return

        if not self.module.file.endswith('admin.py'):
            # Admin classes not in an app's admin.py can cause circular import
            # problems throughout a project.
            #
            # This is because registering an admin class implies a call to
            # models.get_apps() which attempts to import *every* models.py in
            # the project.
            #
            # Whilst your project should probably not have significant
            # inter-app dependencies, importing every possible models.py does
            # not help the situation and can cause ImportError when models are
            # loaded in different scenarios.
            self.add_message('W8020', node=node, args=(node.name,))
