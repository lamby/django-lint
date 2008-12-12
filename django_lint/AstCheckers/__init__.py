__all__ = ('register',)

def register(linter):
    from model_fields import ModelFieldsChecker
    from settings import SettingsChecker

    linter.register_checker(ModelFieldsChecker(linter))
    linter.register_checker(SettingsChecker(linter))
