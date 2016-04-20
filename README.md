Strongly recommend to use linux for development

# Installation

checkout project, and make sure the folder name with the project is not `kio_cal` (see http://stackoverflow.com/a/6949892/1826120)

1. install `python` and `pip`
1. run `pip install -r REQUIREMENTS.txt`
1. run `./manage.py syncdb --all` and create superuser when suggested
1. run `./manage.py migrate --fake`
1. run `./manage.py shell` and type:
  * `import django`
  * `django.contrib.sites.models.Site.objects.create(name='KIO Calendar', domain='SITE.DOMAIN.COM')`

# Run development server
To run development server:  `./manage.py runserver`

# Deploy
https://docs.djangoproject.com/en/1.7/howto/deployment/
