# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django import forms
from django.db.models import Q
from kio_cal.models import ReleaseArticleMembership
from models import Article,Rubric,Release
from redactor.widgets import JQueryEditor
from shared.better_raw_id import ImproveRawIdFieldsForm, ImproveRawIdFieldsFormMixin

class ArticleAdminForm(forms.ModelForm):
    body = forms.CharField( widget=JQueryEditor() )

class ReleaseArticleMembershipInline(admin.TabularInline,ImproveRawIdFieldsFormMixin):
    model = ReleaseArticleMembership
    extra = 1
    order = forms.HiddenInput()
    raw_id_fields = ('article',)

class ArticleAdmin(ImproveRawIdFieldsForm):
    actions = None
    form = ArticleAdminForm
    formfield_overrides = {models.TextField: {'widget': JQueryEditor}}
    list_display = ['title' ,'rubric', 'created_dt',
                    'is_ready','is_published_display']
    search_fields = [ 'authors__last_name',
                      'authors__first_name','title','body']
    raw_id_fields = ['authors']
    readonly_fields = ('is_published_display',)
    list_filter = ['rubric', 'status_db']
    list_select_related = True

    def get_form(self, request, obj=None, **kwargs):
        # save the currently logged in user for later
        self.current_user = request.user
        return super(ArticleAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, field, **kwargs):
        if field and field.name == 'authors':
            kwargs.update({'initial':[self.current_user]})

        return super(ArticleAdmin, self).formfield_for_dbfield(field, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ArticleAdmin,self).get_readonly_fields(
                                                    request,
                                                    obj)
        if obj and obj.is_published():
            return ('is_ready',)+readonly_fields
        else:
            return readonly_fields

#    FIXME: ssdsdsdsdsd
#    def __init__(self,*args,**kwargs):
#        request = kwargs.pop('request')
#        super(ArticleAdmin,self,*args,**kwargs).__init__();
#        self.rubric = forms.ModelChoiceField(
#            choices=Rubric.objects.filter(authors__in=[request.user]))

    def queryset(self, request):
        qs = super(ArticleAdmin, self).queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='editor'):
            return qs
        return qs.filter(Q(authors__in=[request.user]) |
                         Q(rubric__authors__in=[request.user]))

class RubricAdmin(ImproveRawIdFieldsForm):
    list_display = ['title', 'id']
    search_fields = ['id','title']
    raw_id_fields = ['authors']
    filter_vertical = ['authors']
    fields = ['title','authors']

    def queryset(self, request):
        qs = super(RubricAdmin, self).queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='editor'):
            return qs
        return qs.filter(authors__in=[request.user])

class ReleaseForm(forms.ModelForm):
    class Media:
        js = (
            'http://yandex.st/jquery/1.6.4/jquery.min.js',
            'http://yandex.st/jquery-ui/1.8.16/jquery-ui.min.js',
            'js/article-order.js?v2',
        )

class ReleaseAdmin(admin.ModelAdmin):
    form = ReleaseForm
    list_display = ['publication_ts',
                    'is_ready','is_published','id']
    search_fields = ['pk','publication_ts']
    readonly_fields = ['is_published']
    inlines = [ReleaseArticleMembershipInline]

admin.site.register(Article,ArticleAdmin)
admin.site.register(Rubric,RubricAdmin)
admin.site.register(Release,ReleaseAdmin)