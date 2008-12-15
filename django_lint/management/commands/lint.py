from optparse import make_option


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

        from pylint import checkers, lint
        from django_lint import AstCheckers

        linter = lint.PyLinter()
        linter.set_option('reports', options['report'])

        """
        checkers.initialize(linter)
        for msg in ('C0111', 'C0301'):
            linter.disable_message(msg)
        """

        # Register custom checkers
        AstCheckers.register(linter)

        linter.check([name, 'settings'])
