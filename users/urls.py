from django.conf.urls import patterns, url
from .views import ProfileView, ProfileEditView

urlpatterns = patterns('',
                       url(r'^profile/$', ProfileView.as_view(), name='users.profile_detail'),
                       url(r'^profile/edit/(?P<pk>\d+)/$', ProfileEditView.as_view(), name='users.profile_edit'),
                       )




