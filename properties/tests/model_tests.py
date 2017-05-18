from unittest import TestCase
from django.contrib.auth.models import User
from django_dynamic_fixture import G
from homesoko.apps.properties.models import Property, City, Neighbourhood, Feature


class PropertyModelTest(TestCase):
    def test_creating_property(self):
        city = G(City)
        neighbourhood = G(Neighbourhood)
        feature1 = G(Feature)
        feature2 = G(Feature)
        features = [feature1.id, feature2.id]
        user = G(User)
        sokoproperty = Property.objects.create(name='Valdebebas Apartment', price=1000000,
                                                    property_type=Property.PropertyTypeOptions.Apartment,
                                                    category=Property.CategoryOptions.Sale,
                                                    bedrooms=Property.BedroomOptions.Two,
                                                    bathrooms=Property.BathroomsOptions.One,
                                                    description='Spacious apartment in Nairobi', structure_size=1243,
                                                    lot_size=123.34, city=city, neighbourhood=neighbourhood, agency=user
                                                    )
        self.assertEqual(sokoproperty.state, 'new')
        self.assertEqual(sokoproperty.status_percentage, 0)
        sokoproperty.features = features
        self.assertEqual(sokoproperty.status_percentage, 50)
