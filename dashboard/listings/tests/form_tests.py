from unittest import TestCase
from django_dynamic_fixture import G
from homesoko.apps.properties.models import Property, City, Neighbourhood, Feature
from homesoko.apps.dashboard.listings.forms import PropertyForm


class PropertyCreateFormTests(TestCase):
    def test_property_create_form(self):
        city = G(City)
        neighbourhood = G(Neighbourhood)
        feature1 = G(Feature)
        feature2 = G(Feature)
        features = [feature1.id, feature2.id]
        data = {'name': 'Miotoni Apartment',
                'price': 82003000,
                'property_type': Property.PropertyTypeOptions.Apartment,
                'category': Property.CategoryOptions.Sale,
                'bedrooms': Property.BedroomOptions.Two,
                'bathrooms': Property.BathroomsOptions.One,
                'description': 'Spacious home in the cool of Karen',
                'structure_size': 1243,
                'lot_size': 123.34,
                'city': city.id,
                'neighbourhood': neighbourhood.id,
                'features': features
                }
        form = PropertyForm(data, instance=None)
        self.assertTrue(form.is_valid())

