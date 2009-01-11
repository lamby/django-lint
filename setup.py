#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django_lint',
    packages=[
        'DjangoLint',
        'DjangoLint.AstCheckers',
    ],
    scripts='django-lint',
    author='Chris Lamb',
    author_email='chris@chris-lamb.co.uk',
)
