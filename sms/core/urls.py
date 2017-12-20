from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^databases/', views.databases),
    url(r'^messages/', include('messages.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
