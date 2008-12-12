# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django_lint',
    packages=[
        'django_lint',
        'django_lint.management',
        'django_lint.management.commands',
        'django_lint.AstCheckers',
    ],
)
