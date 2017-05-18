from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem
from author.decorators import with_author
from autoslug import AutoSlugField
from sorl.thumbnail import get_thumbnail
from django_fsm import FSMField, transition
from phonenumber_field.modelfields import PhoneNumberField
from time import time

from django.db import models
from geoposition import Geoposition
from geoposition.fields import GeopositionField

@with_author
class City(TimeStampedModel):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name_plural = 'Cities'

    def __unicode__(self):
        return self.name


@with_author
class Neighbourhood(TimeStampedModel):
    name = models.CharField(max_length=20)
    city = models.ForeignKey(City, null=False, blank=False)

    def __unicode__(self):
        return self.name


class SalePropertiesManager(models.Manager):
    def get_queryset(self):
        return super(SalePropertiesManager, self).get_queryset().filter(state=Property.StatesOptions.Published, category=Property.CategoryOptions.Sale)


class LettingPropertiesManager(models.Manager):
    def get_queryset(self):
        return super(LettingPropertiesManager, self).get_queryset().filter(state=Property.StatesOptions.Published, category=Property.CategoryOptions.Letting)

@with_author
class Feature(TimeStampedModel):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



@with_author
class Property(TimeStampedModel):

    class StatesOptions(DjangoChoices):
        New = ChoiceItem('new', 'New')
        FeaturesAdded = ChoiceItem('features_added', 'Features Added')
        ImagesAdded = ChoiceItem('images_added', 'Images Added')
        DocumentsAdded = ChoiceItem('documents_added', 'Documents Added')
        AwaitingAdminApproval = ChoiceItem('awaiting_admin_approval', 'Awaiting Admin Approval')
        Published = ChoiceItem('published', 'Published')
        Inactive = ChoiceItem('inactive', 'Inactive')

    class PropertyTypeOptions(DjangoChoices):
        Apartment = ChoiceItem('apartment', 'Apartment')
        House = ChoiceItem('house', 'House')
        Office = ChoiceItem('office', 'Office')
        Land = ChoiceItem('land', 'Land')
        Townhouse = ChoiceItem('townhouse', 'Townhouse')

    class CategoryOptions(DjangoChoices):
        Letting = ChoiceItem('letting', 'Letting')
        Sale = ChoiceItem('sale', 'For Sale')

    class BedroomOptions(DjangoChoices):
        One = ChoiceItem(1, '1')
        Two = ChoiceItem(1, '2')
        Three = ChoiceItem(3, '3')
        Four = ChoiceItem(4, '4')
        Five = ChoiceItem(5, '5')
        Six = ChoiceItem(6, '6')
        Seven = ChoiceItem(7, '7')
        Eight = ChoiceItem(8, '8')
        Nine = ChoiceItem(9, '9')
        Ten = ChoiceItem(10, '10')
        Eleven = ChoiceItem(11, '11')
        Twelve = ChoiceItem(12, '12')
        Thirteen = ChoiceItem(13, '13')
        Fourteen = ChoiceItem(14, '14')
        Fifteen = ChoiceItem(15, '15')

    class BathroomsOptions(DjangoChoices):
        all_ensuite = ChoiceItem('all_ensuite', 'All Ensuite')
        One = ChoiceItem('1', '1')
        Two = ChoiceItem('2', '2')
        Three = ChoiceItem('3', '3')
        Four = ChoiceItem('4', '4')
        Five = ChoiceItem('5', '5')
        Six = ChoiceItem('6', '6')

    position = GeopositionField()
    name = models.CharField(max_length=20, blank=False)
    slug = AutoSlugField(populate_from='name')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(_('Description'), blank=True, null=True)
    bedrooms = models.IntegerField(max_length=5, null=True, blank=True, choices=BedroomOptions.choices)
    bathrooms = models.CharField(max_length=15, null=True, blank=True, choices=BathroomsOptions.choices)
    structure_size = models.PositiveIntegerField(null=True, blank=True,
                                                 help_text='Size of the structure in square feet')
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                   help_text='Size of the lot in acres')
    city = models.ForeignKey(City, null=False, blank=False)

    neighbourhood = models.ForeignKey(Neighbourhood, null=False, blank=False)
    category = models.CharField(max_length=14, blank=True, choices=CategoryOptions.choices)
    property_type = models.CharField(max_length=20, blank=True, choices=PropertyTypeOptions.choices, default="land")
    agency = models.ForeignKey(User, null=False, blank=False, related_name='property')
    features = models.ManyToManyField(Feature, related_name='property', null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    state = FSMField(default=StatesOptions.New, choices=StatesOptions.choices)
    objects = models.Manager()
    sale = SalePropertiesManager()
    letting = LettingPropertiesManager()

    class Meta:
        verbose_name_plural = 'Properties'

    def __unicode__(self):
        return '%s' % self.name

    # State Transitions
    @transition(field=state, source=[StatesOptions.New, StatesOptions.ImagesAdded], target=StatesOptions.FeaturesAdded)
    def mark_features_added(self):
        pass

    @transition(field=state, source=[StatesOptions.New, StatesOptions.FeaturesAdded], target=StatesOptions.ImagesAdded)
    def mark_images_added(self):
        pass

    @transition(field=state, source=[StatesOptions.New, StatesOptions.DocumentsAdded], target=StatesOptions.DocumentsAdded)
    def mark_documents_added(self):
        pass

    @transition(field=state, source=[StatesOptions.FeaturesAdded, StatesOptions.ImagesAdded, StatesOptions.DocumentsAdded], target=StatesOptions.AwaitingAdminApproval)
    def mark_awaiting_admin_approval(self):
        pass

    @transition(field=state, source=StatesOptions.AwaitingAdminApproval, target=StatesOptions.Published)
    def mark_published(self):
        pass

    @transition(field=state, source='*', target=StatesOptions.Inactive)
    def mark_inactive(self):
        pass

    @property
    def status_percentage(self):
        status_percentage = 0

        if self.state == self.StatesOptions.Published:
            status_percentage = 100
        else:
            if self.features.all():
                status_percentage += 33
            if self.images.all():
                status_percentage += 33
            if self.documents.all():
                status_percentage += 34

        return status_percentage

    @property
    def details(self):
        beds = self.bedrooms if self.bedrooms else '-'
        baths = self.bathrooms if self.bathrooms else '-'
        return "Price: %d,Category: %s,Type: %s,Location: %s-%s,Beds: %s,Baths: %s" % (self.price, self.category, self.property_type, self.neighbourhood, self.city, beds, baths)

    def primary_image_thumbnail(self):
        if self.primary_image():
            return get_thumbnail(self.primary_image().file, '225x225', crop='center', quality=99)
        return None

    def slider_image(self):
        if self.primary_image():
            return get_thumbnail(self.primary_image().file, '1440x600', crop='center', quality=99)
        return None

    def get_missing_image(self):
        pass

    def primary_image(self):
        images = self.images.filter(deleted=False)
        try:
            return images[0]
        except IndexError:
            return None


# class PointOfInterest(models.Model):
#     name = models.CharField(max_length=100)
#     position = GeopositionField()

class PropertyImage(TimeStampedModel):
    file = models.ImageField("File", upload_to="images", max_length=255)
    property = models.ForeignKey(Property, related_name='images', verbose_name=_("Property"))
    caption = models.CharField(_("Caption"), max_length=200, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('property', 'file')
        verbose_name = _('Property Image')
        verbose_name_plural = _('Property Images')

    def __unicode__(self):
        return u"Image of '%s'" % self.property

    def delete(self):
        self.deleted = True
        self.save()


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class PropertyDocuments(TimeStampedModel):
    file = models.FileField("document", upload_to=get_upload_file_name, max_length=255)
    property = models.ForeignKey(Property, related_name="documents", verbose_name=_("Property"))
    caption = models.CharField(_("Caption"), max_length=200, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = ('property', 'file')
        verbose_name = _('Property Document')
        verbose_name_plural = _('Property Documents')

    def __unicode__(self):
        return u"File of '%s'" % self.property

    def delete(self):
        self.deleted = True
        self.save()



@with_author
class PropertyMessage(TimeStampedModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    message = models.TextField()
    property = models.ForeignKey(Property, null=False, blank=False)
    sent = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.name

