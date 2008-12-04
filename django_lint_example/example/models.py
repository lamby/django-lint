from django.db import models

class LintModel(models.Model):
    nullable_charfield = models.CharField(max_length=100, null=True)
