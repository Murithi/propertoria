from selectable.base import LookupBase
from selectable.registry import registry
from .models import Neighbourhood, City


class NeighbourhoodLookup(LookupBase):

    def get_query(self, request, term):
        neighbourhoods = Neighbourhood.objects.all()
        cities = City.objects.all()
        if term.strip() != '':
            neighbourhoods = neighbourhoods.filter(name__icontains=term)
            cities = cities.filter(name__icontains=term)
        cities = [city for city in cities]
        neighbourhoods = [neighbourhood for neighbourhood in neighbourhoods]
        locations = cities + neighbourhoods
        return locations


registry.register(NeighbourhoodLookup)
