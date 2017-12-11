from django.conf.urls import patterns, include, url

urlpatterns = patterns('messages.views',
    url(r'^$', 'index'),
    url(r'^(?P<handle_id>\d+)/$', 'messages'),
    url(r'^(?P<handle_id>\d+)/(?P<filter_day>\d+)/$', 'messages_filtered'),
)
