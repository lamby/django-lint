from optparse import make_option
from pylint import checkers, lint

from django.core.management.base import AppCommand

class Command(AppCommand):
    option_list = AppCommand.option_list + (
        make_option('--report', action='store_true', dest='report',
            help='Generate report (--reports=yes pylint option)',
            default=False),
    )
    help = "Source code analyser for Django apps"
    args = "[appname ...]"

    def handle_app(self, app, **options):
        name = app.__name__.rsplit('.', 1)[0]

        linter = lint.PyLinter()
        linter.set_option('reports', options['report'])
        checkers.initialize(linter)
        linter.disable_message('C0111') # Missing docstring is just
        linter.check(name)
