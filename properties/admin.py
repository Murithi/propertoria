from django.contrib import admin
from .models import Property, City, Neighbourhood, Feature, PropertyMessage


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category', 'city', 'neighbourhood')


class PropertyMessageAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'phone_number', 'email', 'message', 'sent')

admin.site.register(Property, PropertyAdmin)
admin.site.register(City)
admin.site.register(Neighbourhood)
admin.site.register(Feature)
admin.site.register(PropertyMessage, PropertyMessageAdmin)
