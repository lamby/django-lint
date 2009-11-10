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

Templates
=========

 * {% if foo %}{{ foo }}{% else %}bar{% endif %} => {{ foo|default:"bar" }}
 * {% with foo as bar %} ... [ not using {{ bar }} ] ... {% endwith %}
 * {% endblock %} vs. {% endblock blockname %}

settings module:
 * Ordering of MIDDLEWARE_CLASSES
 * TEMPLATE_DIRS not absolute
