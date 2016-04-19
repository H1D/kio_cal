from django.contrib import admin
from django.db.models import TextField
from redactor.widgets import JQueryEditor


class RedactorModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': JQueryEditor},
    }

    class Media:
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js', )

