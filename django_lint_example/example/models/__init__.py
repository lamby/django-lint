from django.db import models

TRUE_VALUE = True

class LintModel(models.Model):
    nullable_charfield = models.CharField(max_length=100, null=True)
    nullable_charfield_2 = models.CharField(max_length=100, null=TRUE_VALUE)
    charfield = models.CharField(max_length=100)

    parent = models.ForeignKey('self')

class Model1(models.Model):
    pass
class Model2(models.Model):
    pass
class Model3(models.Model):
    pass
class Model4(models.Model):
    pass
class Model5(models.Model):
    pass
class Model6(models.Model):
    pass
class Model7(models.Model):
    pass
class Model8(models.Model):
    pass
class Model9(models.Model):
    pass
