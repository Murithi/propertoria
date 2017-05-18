from django.conf.urls import patterns, include, url
from properties.views import Homepage, AboutUs
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Homepage.as_view(), name='home'),
    url(r'^about$', AboutUs.as_view(), name='about'),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^properties/', include('properties.urls')),
    url(r'^dashboard/listings/', include('dashboard.listings.urls')),
    #url(r'^accounts/', include('userena.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^zoner/', include('zoner.urls')),
    url(r'^about/$', TemplateView.as_view(template_name="partialsabout.html")),
)

import os
urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)
