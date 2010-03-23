from django.db import models
from django.contrib import admin

class NullableModel(models.Model):
    TRUTH_VALUE = True

    charfield = models.CharField(max_length=100, null=True, blank=True)
    charfield_2 = models.CharField(max_length=100, null=TRUTH_VALUE)
    textfield = models.TextField(null=True, blank=True)

    boolean_false = models.BooleanField(default=True)

    nullable_boolean = models.NullBooleanField()

    # We should still report about the following field, but we cannot
    # determine its name.
    models.NullBooleanField()

class UniqueForModels(models.Model):
    time = models.DateTimeField()
    u_date = models.IntegerField(unique_for_date='time')
    u_month = models.IntegerField(unique_for_month='time')
    u_year = models.IntegerField(unique_for_year='time')

class ParentModel(models.Model):
    parent = models.ForeignKey('self')

class StrModel(models.Model):
    dummy = models.CharField(max_length=1)

    def __str__(self):
        return "__str__ method"

    def __unicode__(self):
        return self.dummy

class NullBlankModel(models.Model):
    number = models.IntegerField(blank=True)

class BigModel(models.Model):
    field01 = models.IntegerField()
    field02 = models.IntegerField()
    field03 = models.IntegerField()
    field04 = models.IntegerField()
    field05 = models.IntegerField()
    field06 = models.IntegerField()
    field07 = models.IntegerField()
    field08 = models.IntegerField()
    field09 = models.IntegerField()
    field10 = models.IntegerField()
    field11 = models.IntegerField()
    field12 = models.IntegerField()
    field13 = models.IntegerField()
    field14 = models.IntegerField()
    field15 = models.IntegerField()
    field16 = models.IntegerField()
    field17 = models.IntegerField()
    field18 = models.IntegerField()
    field19 = models.IntegerField()
    field20 = models.IntegerField()
    field21 = models.IntegerField()
    field22 = models.IntegerField()
    field23 = models.IntegerField()
    field24 = models.IntegerField()
    field25 = models.IntegerField()
    field26 = models.IntegerField()
    field27 = models.IntegerField()
    field28 = models.IntegerField()
    field29 = models.IntegerField()
    field30 = models.IntegerField()
    field31 = models.IntegerField()

class NoFieldsModel(models.Model):
    pass

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    views = models.PositiveSmallIntegerField()
    words = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post)
    url = models.URLField()

    def __unicode__(self):
        return self.url

class MisorderedMethodsModel(models.Model):
    dummy = models.CharField(max_length=1)

    def incorrect_place(self):
        pass

    def get_absolute_url(self):
        pass

    def __unicode__(self):
        # This should be swapped with get_absolute_url
        pass

    def correct_place(self):
        pass

class Model1(models.Model):
    dummy = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'right'

    def __unicode__(self):
        return self.dummy

class Model2(models.Model):
    dummy = models.CharField(max_length=1)

    def __unicode__(self):
        return self.dummy

    class Meta:
        verbose_name_plural = 'wrong'

class Model3(models.Model):
    class Meta:
        verbose_name_plural = 'wrong'

    dummy = models.CharField(max_length=1)

    def __unicode__(self):
        return self.dummy

class Model4(models.Model):
    dummy = models.CharField(max_length=1)

    def __unicode__(self):
        return self.dummy

class Model5(models.Model):
    dummy = models.CharField(max_length=1)

    def get_absolute_url(self):
        return "/"

    def __unicode__(self):
        return self.dummy

class AbstractModel(models.Model):
    foo = models.CharField(max_length=1)

    class Meta:
        abstract = True

class DerivedModel(AbstractModel):
    bar = models.CharField(max_length=1)

class WeirdPrimaryKeyModel(models.Model):
    primary_key = models.ForeignKey(Model1, primary_key=True)
    unique_field = models.ForeignKey(Model2, unique=True)
    not_both = models.ForeignKey(Model3, primary_key=True, unique=False)

class ManyToManyModel(models.Model):
    nullable = models.ManyToManyField(Model2, null=True)
    blank = models.ManyToManyField(Model3, blank=True)

class AdminKlass(admin.ModelAdmin):
    search_fields = ('nullable',)

    class Meta:
        model = ManyToManyModel
