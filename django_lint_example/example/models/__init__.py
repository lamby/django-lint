from django.db import models

TRUE_VALUE = True

class MyModel(models.Model):
    nullable_charfield = models.CharField(max_length=100, null=True)
    nullable_charfield_2 = models.CharField(max_length=100, null=TRUE_VALUE)

    charfield = models.CharField(max_length=100)

    parent = models.ForeignKey('self')

    def __str__(self):
        return "__str__ method"

class NullBlankModel(models.Model):
    number = models.IntegerField(blank=True)

class BigModel(models.Model):
    field01 = models.CharField(max_length=100)
    field02 = models.CharField(max_length=100)
    field03 = models.CharField(max_length=100)
    field04 = models.CharField(max_length=100)
    field05 = models.CharField(max_length=100)
    field06 = models.CharField(max_length=100)
    field07 = models.CharField(max_length=100)
    field08 = models.CharField(max_length=100)
    field09 = models.CharField(max_length=100)
    field10 = models.CharField(max_length=100)
    field11 = models.CharField(max_length=100)
    field12 = models.CharField(max_length=100)
    field13 = models.CharField(max_length=100)
    field14 = models.CharField(max_length=100)
    field15 = models.CharField(max_length=100)
    field16 = models.CharField(max_length=100)
    field17 = models.CharField(max_length=100)
    field18 = models.CharField(max_length=100)
    field19 = models.CharField(max_length=100)
    field20 = models.CharField(max_length=100)
    field21 = models.CharField(max_length=100)
    field22 = models.CharField(max_length=100)
    field23 = models.CharField(max_length=100)
    field24 = models.CharField(max_length=100)
    field25 = models.CharField(max_length=100)
    field26 = models.CharField(max_length=100)
    field27 = models.CharField(max_length=100)
    field28 = models.CharField(max_length=100)
    field29 = models.CharField(max_length=100)
    field30 = models.CharField(max_length=100)

class NoFieldsModel(models.Model):
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
