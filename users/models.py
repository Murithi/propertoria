from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author
from autoslug import AutoSlugField


@with_author
class Profile(TimeStampedModel):
    user = models.OneToOneField(User, related_name='profile')
    company = models.CharField(max_length=30, blank=True)
    slug = AutoSlugField(populate_from='company', blank=True)

    def __unicode__(self):
        return "User: " + str(self.user) + ", Company: " + str(self.company)

    @classmethod
    def create(cls, user):
        profile = Profile.objects.create(user=user)
        return profile
