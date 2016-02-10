from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from kio_cal.feeds import FullFeed, RubricFeed

urlpatterns = patterns('kio_cal.views',
    url(r'^$', 'frontpage',
        name="frontpage"),
    url('^(?P<pk>\d+)/$', 'release',
        name="release"),
    url('^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<count>\d)?(/)?$',
        'release_by_date',
        name='release_by_date'),
    url('^article/(?P<pk>\d+)/$', 'article',
        name="article_full"),
)

urlpatterns += patterns('',
    url(r'^rss/$', FullFeed(),
        name='rss_feed'),
    url(r'^rubric/(?P<rubric_id>\d)/rss/$', RubricFeed(),
        name='rubric_rss_feed'),
)