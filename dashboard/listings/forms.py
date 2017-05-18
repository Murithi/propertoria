from django import forms
from django.conf import settings
from properties.models import Property, City, Neighbourhood, Feature
from django.forms.models import ModelMultipleChoiceField


# Thanks to http://stackoverflow.com/questions/8630977/manytomany-field-in-form-with-checkboxes-insted-select-field-in-django-template
class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class AddPropertyFeaturesForm(forms.ModelForm):
    features = CustomSelectMultiple(widget=forms.CheckboxSelectMultiple, queryset=Feature.objects.all())

    class Meta:
        fields = ('features',)
        model = Property


class PropertyForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={'required':'The name of the property is required'})
    price = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    property_type = forms.ChoiceField(choices=Property.PropertyTypeOptions.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=Property.CategoryOptions.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    bedrooms = forms.ChoiceField(choices=Property.BedroomOptions.choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    bathrooms = forms.ChoiceField(choices=Property.BathroomsOptions.choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))
    structure_size = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Size of the structure in square feet',
                                        required=False)
    lot_size = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Size of the lot in acres',
                                  required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    neighbourhood = forms.ModelChoiceField(queryset=Neighbourhood.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Property
        exclude = ['author', 'updated_by', 'features', 'agency', 'is_premium', 'is_featured', 'state']


class LandForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'The name of the property is required'})
    price = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=Property.CategoryOptions.choices,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    lot_size = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  help_text='Size of the land in acres',
                                  required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))

    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    neighbourhood = forms.ModelChoiceField(queryset=Neighbourhood.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Property
        fields =  ['name', 'price', 'features', 'category', 'lot_size', 'description', 'city', 'neighbourhood']

