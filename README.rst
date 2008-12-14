django-lint
"""""""""""

Ideas
=====

 * Detecting default managers
 * Determining whether you have a poor code/applications ratio.
 * Oldforms (?)
 * Overring definition of model. Eg:
    class MyModel(models.Model):
    	foo = [..]
	foo = [..]
 * Non-absolute template_dirs
 * Missing __unicode__ (?)
 * Not importing settings via "django.conf import settings"
 * No related_name
 * Not using reverse (or @permalink) in get_absolute_url (?)

Templates
=========

 * {% if foo %}{{ foo }}{% else %}bar{% endif %} => {{ foo|default:"bar" }}
 * {% with foo as bar %} ... [ not using {{ bar }} ] ... {% endwith %}
 * {% endblock %} vs. {% endblock blockname %}

settings module:
 * Ordering of MIDDLEWARE_CLASSES
 * TEMPLATE_DIRS not absolute
