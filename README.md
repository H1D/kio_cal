Strongly recommend to use linux for development

# installation
1. install `python` and `pip`
1. run `pip install -r REQUIREMENTS.txt`
1. run `./manage.py sync --all` and create superuser when suggested
1. run `./manage.py migrate --fake`
1. run `./manage.py shell` and type: `import django;django.contrib.sites.models.Site.objects.create(name='example.cdom', domain='example.codm')`

# run development server
To run development server:  `./manage.py runserver`
