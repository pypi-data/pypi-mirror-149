import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# User model extended as per
# https://web.archive.org/web/20220204223759/https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    email_confirmed = models.BooleanField(default=False)

    # extra fields to populate from LDAP/AD
    affiliation = models.CharField(max_length=255, blank=False)
    orcid = models.CharField(
        max_length=100, blank=False, null=False, default="-"
    )


# auto-create the profile associated with this user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_django_user_profile(sender, instance, created, **kwargs):
    """
    A new django_user has been created, ensure a profile object has been too.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # if the user has just been created, ensure the django profile has been too
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
