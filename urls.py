import os

from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^untitled/', include('untitled.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'', include('kio_cal.urls')),
    url(r'', include('redactor.urls')),
    url(r'', include('invitation.urls')),
)

if settings.DEBUG or True:
    urlpatterns += patterns("django.views.static",
        url(r"^%s/(?P<path>.*)$" % settings.MEDIA_URL.strip('/'), "serve",
            {"document_root": settings.MEDIA_ROOT}),
#
##        url(r"^%s/(?P<path>.*)$" % settings.MEDIA_URL.strip('/'), "serve",
##            {"document_root": settings.MEDIA_ROOT}),
##        url(r"^img/(?P<path>.*)$", "serve",
##            {"document_root": os.path.join(settings.MEDIA_ROOT, 'img')}),
##        url(r"^(?P<path>.*)$", "serve",
##            {"document_root": os.path.join(settings.MEDIA_ROOT,'jscolor')}),
##        url(r"^(?P<path>.*)$", "serve",
##            {"document_root": os.path.join(settings.MEDIA_ROOT,'cache')}),
    )
    pass