from django.conf.urls import patterns, url
from .views import BaseView

urlpatterns = patterns('',
                       url(r'^base/$', BaseView.as_view(), name='zoner.zoner_base'),
                       )



