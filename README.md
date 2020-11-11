# `django-lint`

## Important notice

This project has been 2008 and was maintained until 2011; it has since been
deprecated. If you wish to check out similar functionality, please see:

* Richard Tier's [Django Doctor](https://django.doctor/)

## Ideas

### General

* Default manager with restrictive get\_query\_set()
* Oldforms (?)
* Overriding definition of model. e.g.:

     class MyModel(models.Model):

     :   foo = \[..\]

     foo = \[..\]

* Not importing settings via \"django.conf import settings\"
* Not using reverse (or \@permalink) in get\_absolute\_url (?)
* Form definitions in models.py
* Ignore tests

### Models

* Don\'t count ManyToMany fields on a model as a field
> Remove common prefix checking.
>   models.. specifying \"objects = \" should be last

### Views

* Calling request.is\_authenticated without actually calling
>     function
* order\_by(\'?\')
* request.method.upper is a no-op (etc.)
* cache.set without a timeout

### URLS

* Unreversible urlpatterns

#### Layout

> -   Form class not in forms.py
> -   Admin class not in admin.py

#### Templates

* {% if foo %}{{ foo }}{% else %}bar{% endif %} =\> {{
  foo\|default:\"bar\" }}
* {% with foo as bar %} \... \[ not using {{ bar }} \] \... {%
   endwith %}
* {% endblock %} vs. {% endblock blockname %}

#### Settings

* Ordering of MIDDLEWARE\_CLASSES
* `TEMPLATE_DIRS` not absolute

#### Layout

* forms not in forms.py managers not in managers.py
