from django.db import models

TRUE_VALUE = True

class LintModel(models.Model):
    nullable_charfield = models.CharField(max_length=100, null=True)
    nullable_charfield_2 = models.CharField(max_length=100, null=TRUE_VALUE)
    charfield = models.CharField(max_length=100)
