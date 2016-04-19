# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.text import truncate_html_words
from kio_cal.models import Article, Release, Rubric

class FullFeed(Feed):
    title = u'КИО календарь'
    link = '/'
    description = u'Все статьи КИО календарь'

    def items(self):
        return Release.objects.order_by('-publication_ts')[0].articles()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncate_html_words(item.body,25)

    def item_link(self, item):
        return item.get_absolute_url()

class RubricFeed(Feed):
    def get_object(self, request, rubric_id):
        return get_object_or_404(Rubric, pk=rubric_id)

    def title(self, obj):
        return u'КИО | %s' % obj.title

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncate_html_words(item.body,25)

    def item_link(self, item):
        return item.get_absolute_url()

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return u'КИО календарь. Статьи из рубрики   %s' % obj.title

    def items(self, obj):
        return Article.objects.filter(rubric=obj).order_by('-modified_dt')