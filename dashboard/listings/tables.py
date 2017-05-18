from django.utils.safestring import mark_safe
import django_tables2 as tables
from properties.models import Property


class PropertyTable(tables.Table):

    class Meta:
        model = Property
        fields = ('name', 'details')

    def render_details(self, value):
        return mark_safe(value.replace(',', '\n'))

