from django.contrib.markup.templatetags.markup import markdown
from django.core.management import BaseCommand
from kio_cal.models import Article

class Command(BaseCommand):

    def execute(self, *args, **options):
        for a in Article.objects.all():
            a.save()