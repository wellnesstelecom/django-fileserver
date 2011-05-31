# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^translations/(?P<basename>\S+)/$', 'fileserver.views.serve'),
)
