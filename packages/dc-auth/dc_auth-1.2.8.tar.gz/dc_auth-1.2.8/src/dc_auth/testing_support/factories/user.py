"""Model factories for the User model"""
import datetime as dt
from random import randint

from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
import faker
import factory
import factory.django
from factory import (
    lazy_attribute,
    BUILD_STRATEGY,
)
import pytz

from . import SECURE_PASSWORD

faker = faker.Factory.create()  # separate to a factory boy Factory


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "dc_auth.Profile"
        strategy = BUILD_STRATEGY

    affiliation = lazy_attribute(lambda o: faker.company())
    orcid = lazy_attribute(lambda o: faker.phone_number())

    email_confirmed = False

    # We pass in profile=None to prevent UserFactory from creating another
    # profile (this disables the RelatedFactory)
    user = factory.SubFactory(
        "dc_auth.testing_support.factories.user.UserFactory", profile=None
    )


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        strategy = BUILD_STRATEGY
        django_get_or_create = ("username",)

    first_name = lazy_attribute(lambda o: faker.first_name())
    last_name = lazy_attribute(lambda o: faker.last_name())
    username = lazy_attribute(
        lambda o: slugify(o.first_name + "." + o.last_name)
    )
    password = SECURE_PASSWORD  # don't hash the password for testing

    @lazy_attribute
    def email(self):
        domain = (
            "dc.fake.datacentral.org.au"
            if self.is_staff
            else "dc.fake.institution.edu.au"
        )
        return self.username + "@" + domain

    @lazy_attribute
    def date_joined(self):
        return dt.datetime.now(tz=pytz.UTC) - dt.timedelta(days=randint(5, 50))

    last_login = lazy_attribute(lambda o: o.date_joined + dt.timedelta(days=4))

    is_staff = False
    is_active = False
    # We pass in 'user' to link the generated Profile to our just-generated
    # User.
    # This will call ProfileFactory(user=our_new_user), thus skipping the
    # SubFactory.
    profile = factory.RelatedFactory(ProfileFactory, "user")
