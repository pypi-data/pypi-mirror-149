from copy import deepcopy

from django.db import transaction
from django.dispatch import receiver
from django.test import RequestFactory
from django_cas_ng.signals import cas_user_authenticated
import pytest

from .factories import SECURE_PASSWORD


@pytest.fixture
def profile_factory(db):
    from .factories.user import ProfileFactory

    return ProfileFactory


@pytest.fixture
def user_factory(db):
    from .factories.user import UserFactory

    return UserFactory


@pytest.fixture
def profile(profile_factory):
    return profile_factory.create()


@pytest.fixture
def user(profile):
    return profile.user


@pytest.fixture
def affiliation(faker):
    return faker.company()


@pytest.fixture
def secure_password():
    return SECURE_PASSWORD


def add_mock_verification(username, user_attrs, monkeypatch):
    def mock_verify(self, ticket):
        """Mock verification"""
        attrs = deepcopy(user_attrs)
        attrs.update({'ticket': ticket, 'service': 'service_url'})
        proxy_ticket = None
        return username, attrs, proxy_ticket

    # we mock out the verify method so that we can bypass the external http
    # calls needed for real authentication since we are testing the logic
    # around authentication.
    monkeypatch.setattr('cas.CASClientV2.verify_ticket', mock_verify)
    return dict(ticket='fake-ticket', service='fake-service')


def mock_login_cas(monkeypatch, django_user_model, username, user_attrs):
    """

    :param monkeypatch:
    :param django_user_model:
    :param user:
    :return:
    """
    from django_cas_ng.backends import CASBackend

    factory = RequestFactory()
    request = factory.get('/login/')
    request.session = {}

    callback_values = {}

    @receiver(cas_user_authenticated)
    def callback(sender, **kwargs):
        callback_values.update(kwargs)

    auth_kwargs = add_mock_verification(username, user_attrs, monkeypatch)

    # sanity check
    with transaction.atomic():
        assert not django_user_model.objects.filter(
            username=username,
        ).exists()

    with transaction.atomic():
        backend = CASBackend()
        auth_user = backend.authenticate(request=request, **auth_kwargs)

    assert auth_user is not None

    return callback_values, auth_user, request


def create_cas_attrs_from_user(user, override=None):
    """
    Give a similar-enough dictionary of attributes from a CAS response. The
    response can be overridden/expanded by `override`.
    """
    try:
        groups = [
            'CN={},OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU'.format(
                group.name
            ) for group in user.groups.all()
        ]
    except ValueError:
        groups = []

    attrs = {
        'isFromNewLogin': 'false',
        'authenticationDate': '2019-03-07T23:17:23.351Z[UTC]',
        'displayName': '{} {}'.format(user.first_name, user.last_name),
        'successfulAuthenticationHandlers': 'Active Directory',
        'groups': groups,
        'orcid': user.profile.orcid,
        'credentialType': 'UsernamePasswordCredential',
        'authenticationMethod': 'Active Directory',
        'longTermAuthenticationRequestTokenUsed': 'false',
        'last_name': user.last_name,
        'first_name': user.first_name,
        'email': user.email,
    }

    if override is not None:
        attrs.update(override)

    return attrs
