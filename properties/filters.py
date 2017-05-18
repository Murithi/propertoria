import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    city = django_filters.CharFilter(name='city__name')
    neighbourhood = django_filters.CharFilter(name='neighbourhood__name')

    class Meta:
        model = Property
        fields = ['city__name', 'bedrooms', 'bathrooms', 'neighbourhood__name', 'category', 'price', 'property_type']