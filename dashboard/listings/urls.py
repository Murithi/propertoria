from django.conf.urls import url, patterns
from .views import PropertyListView, PropertyCreateView, AddPropertyFeaturesView, PropertyImagesDeleteView, PropertyImagesListView, \
    PropertyImagesUploadView, EditPropertyView, PropertyDocumentsUploadView, PropertyDocumentsListView, PropertyDocumentsDeleteView, \
    LandListView, LandCreateView, EditLandView, LocationView

urlpatterns = patterns('',
    url(r'^$', PropertyListView.as_view(), name='listings.property_list'),
    url(r'^$', LandListView.as_view(), name='listings.land_list'),
    url(r'^new/$', PropertyCreateView.as_view(), name='listings.property_new'),
    url(r'^new/$', LandCreateView.as_view(), name='listings.land_new'),
    url(r'^location/(?P<pk>\d+)/$', LocationView.as_view(), name='listings.location'),
    url(r'^features/(?P<pk>\d+)/$', AddPropertyFeaturesView.as_view(), name='listings.property_features'),
    url(r'^images/(?P<pk>\d+)/$', PropertyImagesUploadView.as_view(), name='listings.images_upload'),
    url(r'^images/delete/(?P<pk>\d+)/$', PropertyImagesDeleteView.as_view(), name='listings.images_delete'),
    url(r'^images/list/(?P<pk>\d+)/$', PropertyImagesListView.as_view(), name='listings.images_view'),
    url(r'^files/(?P<pk>\d+)/$', PropertyDocumentsUploadView.as_view(), name='listings.files_upload'),
    url(r'^files/delete/(?P<pk>\d+)/$', PropertyDocumentsDeleteView.as_view(), name='listings.files_delete'),
    url(r'^files/list/(?P<pk>\d+)/$', PropertyDocumentsListView.as_view(), name='listings.files_view'),
    url(r'^edit/(?P<pk>\d+)/$', EditPropertyView.as_view(), name='listings.property_edit'),
    url(r'^edit/(?P<pk>\d+)/$', EditLandView.as_view(), name='listings.land_edit'),
)
