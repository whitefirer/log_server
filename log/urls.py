from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings
from views.main import *
from core.log import *

urlpatterns = patterns('',

    # sys manage
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.RESOURCES_PATH}),
    url(r'^manage/log/.*$', invoke_template, {'template_name': 'loglist.htm'}),
	url(r'^$', invoke_template, {'template_name': 'loglist.htm'}),
	url(r'^cliapi$', cliapi_action),
    url(r'^cliapi/$', cliapi_action),
    url(r'^api$', api_action),
    url(r'^api/$', api_action),
)
