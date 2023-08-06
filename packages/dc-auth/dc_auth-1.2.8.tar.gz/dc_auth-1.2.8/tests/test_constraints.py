from django.db import IntegrityError
import pytest


@pytest.mark.django_db
def test_duplicate_django_username(profile_factory):
    """
    You cannot have two django accounts with the same username (django
    constraint)
    :return:
    """
    django_users = [p.user for p in profile_factory.create_batch(2)]
    identical_username = django_users[0].username
    django_users[1].username = identical_username
    # we can't save the second django object as it violates django db integrity
    # on User model
    with pytest.raises(IntegrityError) as excinfo:
        django_users[1].save()
    assert 'UNIQUE constraint failed: auth_user.username' in str(excinfo.value)
