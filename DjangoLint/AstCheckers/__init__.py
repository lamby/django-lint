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

__all__ = ('register',)

def register(linter):
    from size import SizeChecker
    from admin import AdminChecker
    from settings import SettingsChecker
    from model_fields import ModelFieldsChecker
    from model_methods import ModelMethodsChecker

    linter.register_checker(SizeChecker(linter))
    linter.register_checker(AdminChecker(linter))
    linter.register_checker(SettingsChecker(linter))
    linter.register_checker(ModelFieldsChecker(linter))
    linter.register_checker(ModelMethodsChecker(linter))
