__all__ = ('register',)

def register(linter):
    from size import SizeChecker
    from settings import SettingsChecker
    from model_fields import ModelFieldsChecker

    linter.register_checker(SizeChecker(linter))
    linter.register_checker(SettingsChecker(linter))
    linter.register_checker(ModelFieldsChecker(linter))
