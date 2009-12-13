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

Models
======

 * Don't count ManyToMany fields on a model as a field
 * Remove common prefix checking.

Views
=====

 * Calling request.is_authenticated without actually calling function
 * order_by('?')

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
