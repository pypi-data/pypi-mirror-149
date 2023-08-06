import pytest


@pytest.mark.django_db
def test_profile_is_profile(profile):
    user = profile.user
    user_profile = user.profile
    assert profile == user_profile


@pytest.mark.django_db
def test_user_is_user(user):
    profile = user.profile
    profile_user = profile.user
    assert user == profile_user


@pytest.mark.django_db
def test_profile_email_not_confirmed(profile):
    assert not profile.email_confirmed


@pytest.mark.django_db
def test_user_is_not_active(user):
    assert not user.is_active


@pytest.mark.django_db
def test_user_is_not_staff(user):
    assert not user.is_staff
