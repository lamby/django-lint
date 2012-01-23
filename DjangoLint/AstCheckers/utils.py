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

from itertools import chain
from pylint.checkers.utils import safe_infer

def is_model(node, **kwargs):
    return nodeisinstance(node, ('django.db.models.base.Model',), **kwargs)

def nodeisinstance(node, klasses, check_base_classes=True):
    if not isinstance(node, astng.Class):
        return False

    for base in node.bases:
        val = safe_infer(base)
        if not val:
            continue
        if isinstance(val, astng.bases._Yes):
            continue

        nodes = [val]
        if check_base_classes:
            try:
                nodes = chain([val], val.ancestors())
            except TypeError:
                pass

        for node in nodes:
            qual = '%s.%s' % (node.root().name, node.name)
            if qual in klasses:
                return True

    return False
