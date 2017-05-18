from django.conf.urls import patterns, url
from .views import LettingPropertiesView, SalePropertiesView, PropertyDetailView, PropertyListView, CityPropertiesView, \
                   NeighbourhoodPropertiesView, agent_message, CompanyPropertiesView, LandListView, SaleLandView, LeasingLandView, \
                   CityLandView, NeighbourhoodLandView

urlpatterns = patterns('',
                       #(r'contact-agent/$',agent_message),

                       # LAND LISTING MANAGEMENT
                       url(r'list-land/$', LandListView.as_view(), name='land.list'),
                       url(r'list-land/for-sale(?:/(?P<type>[\w-]+)/)?$', SaleLandView.as_view(), name='land.land_sale'),
                       url(r'list-land/leasing(?:/(?P<type>[\w-]+)/)?$', LeasingLandView.as_view(),
                           name='land.land_leasing'),
                       url(r'list-land-city/(?P<city>[\w-]+)/(?:/(?P<type>[\w-]+)/)?$', CityLandView.as_view(),
                           name='land.land_city'),
                       url(r'list-neighbourhood/(?P<neighbourhood>[\w-]+)/(?:/(?P<type>[\w-]+)/)?$', NeighbourhoodLandView.as_view(),
                           name='land.land_neighbourhood'),
                       url(r'list/company/(?P<company>[\w-]+)/$', CompanyPropertiesView.as_view(),
                           name='properties.list_company'),
                       url(r'listing/(?P<property_slug>[\w-]+)/$', PropertyDetailView.as_view(),
                           name='properties.listing'),
                       url(r'message/$', agent_message, name='properties.listing_message'),

                       #PROPERTY LISTING MANAGEMENT
                       url(r'list/$', PropertyListView.as_view(), name='properties.list'),
                       url(r'list/for-sale(?:/(?P<type>[\w-]+)/)?$', SalePropertiesView.as_view(), name='properties.list_sale'),
                       url(r'list/letting(?:/(?P<type>[\w-]+)/)?$', LettingPropertiesView.as_view(), name='properties.list_letting'),
                       url(r'list/(?P<city>[\w-]+)/(?:/(?P<type>[\w-]+)/)?$', CityPropertiesView.as_view(), name='properties.list_city'),
                       url(r'list/(?P<neighbourhood>[\w-]+)/(?:/(?P<type>[\w-]+)/)?$', NeighbourhoodPropertiesView.as_view(), name='properties.list_neighbourhood'),
                       url(r'list/company/(?P<company>[\w-]+)/$', CompanyPropertiesView.as_view(), name='properties.list_company'),
                       url(r'listing/(?P<property_slug>[\w-]+)/$', PropertyDetailView.as_view(), name='properties.listing'),
                       url(r'message/$', agent_message, name='properties.listing_message'),


                       )
