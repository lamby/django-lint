django-lint
"""""""""""

Ideas
=====

 * Default manager with restrictive get_query_set()
 * Oldforms (?)
 * Overring definition of model. Eg:
    class MyModel(models.Model):
    	foo = [..]
	foo = [..]
 * Not importing settings via "django.conf import settings"
 * Not using reverse (or @permalink) in get_absolute_url (?)
 * Form definitions in models.py
 * Ignore tests

Models
======

 * Don't count ManyToMany fields on a model as a field
 * Remove common prefix checking.
 * models.. specifying "objects = " should be last

Views
=====

 * Calling request.is_authenticated without actually calling function
 * order_by('?')
 * request.method.upper is a no-op (etc.)
 * cache.set without a timeout

URLS
====

 * Unreversible urlpatterns

Layout
======

 * Form class not in forms.py
 * Admin class not in admin.py

Templates
=========

 * {% if foo %}{{ foo }}{% else %}bar{% endif %} => {{ foo|default:"bar" }}
 * {% with foo as bar %} ... [ not using {{ bar }} ] ... {% endwith %}
 * {% endblock %} vs. {% endblock blockname %}

Settings
========
 * Ordering of MIDDLEWARE_CLASSES
 * TEMPLATE_DIRS not absolute

Layout
======
 forms not in forms.py
 managers not in managers.py
