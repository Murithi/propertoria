import json
from django.views.generic import View, TemplateView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from users.models import Profile
from .models import Property, PropertyMessage
from .filters import PropertyFilter
from .forms import PropertyMessageForm, PropertySearchForm


class Homepage(TemplateView):
    template_name = "home.html"
    search_form = PropertySearchForm

    def get_context_data(self, **kwargs):
        context_data = super(Homepage, self).get_context_data(**kwargs)
        context_data['premium_properties'] = Property.objects.filter(is_premium=True)
        context_data['properties'] = Property.objects.filter(state=Property.StatesOptions.Published)
        context_data['search_form'] = self.search_form
        return context_data

class AboutUs(TemplateView):
    template_name = "aboutus.html"

class PropertyDetailView(DetailView):

    template_name = 'property_detail.html'
    model = Property
    slug_url_kwarg = 'property_slug'
    slug_field = 'slug'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context_data = super(PropertyDetailView, self).get_context_data(**kwargs)
        sokoproperty = self.get_object()
       # assert False, sokoproperty
        if (sokoproperty.property_type == 'land'):
            template_name='land_detail.hmtl'

        context_data['images'] = sokoproperty.images.all()
        context_data['features'] = sokoproperty.features.all()
        context_data['form'] = PropertyMessageForm
        return context_data

class SaleLandView(TemplateView):
    template_name = "land_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(SaleLandView, self).get_context_data(**kwargs)
        land_list = Property.sale.filter(property_type='land')

        # assert False, land_list
        # Pagination
        paginator = Paginator(land_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Land for Lease'
        context_data['page_title'] = 'Land for Sale'
        return context_data

class SalePropertiesView(TemplateView):
    template_name = "property_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(SalePropertiesView, self).get_context_data(**kwargs)
        if kwargs['type']:
            properties_list = Property.sale.filter(property_type=kwargs['type'])
        else:
            properties_list = Property.sale.all()

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Property for letting'
        context_data['page_title'] = 'Properties for sale'
        return context_data


class LeasingLandView(TemplateView):
    template_name = "land_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(LeasingLandView, self).get_context_data(**kwargs)
        # if kwargs['type']:
        #     properties_list = Property.letting.filter(property_type='land')
        # else:
        #     properties_list = Property.letting.all()
        properties_list = Property.letting.filter(property_type='land')
        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Land for Lease'
        return context_data


class LettingPropertiesView(TemplateView):
    template_name = "property_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(LettingPropertiesView, self).get_context_data(**kwargs)
        if kwargs['type']:
            properties_list = Property.letting.filter(property_type=kwargs['type'])
        else:
            properties_list = Property.letting.all()

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Properties for letting'
        return context_data

class CityLandView(TemplateView):
    template_name = "land_list.html"
    def get_context_data(self, **kwargs):
        context_data = super(CityLandView, self).get_context_data(**kwargs)
        city = kwargs['city']

        queryset = Property.objects.filter(state=Property.StatesOptions.Published, city__name=city)
        # if kwargs['type']:
        #     properties_list = queryset.filter(property_type=kwargs['type'])
        # else:
        #     properties_list = queryset
        properties_list = queryset.filter(property_type='land')

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Land in ' + city
        return context_data

class CityPropertiesView(TemplateView):
    template_name = "property_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(CityPropertiesView, self).get_context_data(**kwargs)
        city = kwargs['city']
        queryset = Property.objects.filter(state=Property.StatesOptions.Published, city__name=city)
        if kwargs['type']:
            properties_list = queryset.filter(property_type=kwargs['type'])
        else:
            properties_list = queryset

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Properties in ' + city
        return context_data


class NeighbourhoodLandView(TemplateView):
    template_name = "land_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(NeighbourhoodLandView, self).get_context_data(**kwargs)
        neighbourhood = kwargs['neighbourhood']

        queryset = Property.objects.filter(state=Property.StatesOptions.Published, neighbourhood__name=neighbourhood)
        # if kwargs['type']:
        #     properties_list = queryset.filter(property_type=kwargs['type'])
        # else:
        #     properties_list = queryset
        properties_list = queryset.filter(property_type='land')

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Land in ' + neighbourhood
        return context_data


class NeighbourhoodPropertiesView(TemplateView):
    template_name = "property_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(NeighbourhoodPropertiesView, self).get_context_data(**kwargs)
        neighbourhood = kwargs['neighbourhood']
        queryset = Property.objects.filter(state=Property.StatesOptions.Published, neighbourhood__name=neighbourhood)
        if kwargs['type']:
            properties_list = queryset.filter(property_type=kwargs['type'])
        else:
            properties_list = queryset

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = 'Properties in ' + neighbourhood
        return context_data


class CompanyPropertiesView(TemplateView):
    template_name = "property_list.html"

    def get_context_data(self, **kwargs):
        context_data = super(CompanyPropertiesView, self).get_context_data(**kwargs)
        company = kwargs['company']
        user = Profile.objects.get(company=company).user
        properties_list = user.property.filter(state=Property.StatesOptions.Published)

        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = self.request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        context_data['page_title'] = company + ' properties'
        return context_data

class LandListView(View):
    initial = {'key': 'value'}
    template_name = "property_list.html"

    def get(self, request, *args, **kwargs):
        context_data = {'page_title': 'Property List'}
        properties_list = Property.objects.filter(state=Property.StatesOptions.Published,  property_type='land')
        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = request.GET.get('page')

        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        context_data = {'page_title':  'Property List'}
        properties_list = PropertyFilter(request.POST, queryset=Property.objects.filter(state=Property.StatesOptions.Published,  property_type='land'))
        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        return render(request, self.template_name, context_data)

class PropertyListView(View):
    initial = {'key': 'value'}
    template_name = "property_list.html"

    def get(self, request, *args, **kwargs):
        context_data = {'page_title': 'Property List'}
        properties_list = Property.objects.filter(state=Property.StatesOptions.Published)
        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = request.GET.get('page')

        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        context_data = {'page_title':  'Property List'}
        properties_list = PropertyFilter(request.POST, queryset=Property.objects.filter(state=Property.StatesOptions.Published))
        # Pagination
        paginator = Paginator(properties_list, 24)  # Show 25 listings per page
        page = request.GET.get('page')
        try:
            context_data['properties'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context_data['properties'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context_data['properties'] = paginator.page(paginator.num_pages)

        return render(request, self.template_name, context_data)


def agent_message(request):
    contact_agent_form = PropertyMessageForm(request.POST)
    data = request.POST.copy()
    listing = Property.objects.get(id=data['property'])
    if request.is_ajax():
        if contact_agent_form.is_valid():
            PropertyMessage.objects.create(name=data['name'], phone_number=data['phone'],
                                           email=data['email'], message=data['message'], property=listing)
            response = json.dumps({'success': 'True'})
        else:
            errors = {}
            for e in contact_agent_form.errors.iteritems():
                errors.update({e[0]: unicode(e[1])})
            html = contact_agent_form.errors.as_ul()
            response = json.dumps({'success': 'False', 'html': html, 'errors': errors})
        return HttpResponse(response, mimetype='application/json')
    else:
        if contact_agent_form.is_valid():
            PropertyMessage.objects.create(name=data['name'],phone_number=data['phone'],
                                           email=data['email'],message=data['message'], property=listing)
            messages.add_message(request, messages.INFO, 'Your message has been sent.You will be contacted soon', extra_tags='alert-success')
        else:
            messages.add_message(request, messages.INFO, 'All fields are required!', extra_tags='alert-error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

