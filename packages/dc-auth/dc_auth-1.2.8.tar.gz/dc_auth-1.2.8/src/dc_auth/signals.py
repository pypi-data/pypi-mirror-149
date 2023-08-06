import logging
from django.apps import apps
from django.dispatch import receiver, Signal
from django_cas_ng.signals import cas_user_authenticated

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


cas_user_set_up = Signal()


@receiver(cas_user_authenticated)
def populate_user_model(
    *, user, created, attributes, ticket, service, request, **kwargs
):
    """
    Create the user profile if it hasn't been already, populate orcid,
    get_or_create all groups returned and associate with this user.

    :param user:
    :param created:
    :param attributes: {
        'isFromNewLogin': 'true',
        'authenticationDate': '2019-03-07T23:17:23.351Z[UTC]',
        'displayName': 'Elizabeth Mannering',
        'successfulAuthenticationHandlers': 'Active Directory',
        'groups': [
            'CN=Testing,OU=Groups,OU=Accounts,DC=ASVO,DC=AAO,DC=GOV,DC=AU',
        ],
        'orcid': '-',
        'credentialType': 'UsernamePasswordCredential',
        'authenticationMethod': 'Active Directory',
        'longTermAuthenticationRequestTokenUsed': 'false',
        'last_name': 'Mannering',
        'first_name': 'Elizabeth',
        'email': 'Liz.Mannering@mq.edu.au'
    }
    :param ticket:
    :param service:
    :param request:
    :param kwargs:
    :return:
    """

    if user:
        try:
            # - - - - - - - - - - - Profile - - - - - - - - - - -

            # ensure the profile object exists
            if not hasattr(user, "profile"):
                apps.get_model(
                    app_label="dc_auth", model_name="profile"
                ).objects.create(user=user)
                user.profile.save()

            # custom attributes
            user.profile.orcid = attributes.get("orcid", "-")
            user.profile.affiliation = attributes.get("affiliation")

            # if user is authenticated with CAS, their email confirmation state
            # must be true as users are only pushed to ldap after email
            # confirmation
            user.profile.email_confirmed = True
            user.profile.save()

            # - - - - - - - - - - - Groups - - - - - - - - - - -

            # clear any initial groups, then add back the ones in ldap
            user.groups.clear()
            groups = attributes.get("groups", None)
            if groups:
                if isinstance(groups, str):
                    groups = [groups]
                for group_attr in groups:
                    group_name = group_attr.split("CN=")[1].split(",")[0]

                    group, created = apps.get_model(
                        app_label="auth", model_name="group"
                    ).objects.get_or_create(name=group_name)

                    group.user_set.add(user)
                    if created:
                        logger.info(f"Created {group_name}")
                    logger.info(f"Added {user.username} to {group_name}")

            # - - - - - - - - - - - User - - - - - - - - - - - -
            # ensure passwords are never stored locally
            user.set_unusable_password()

            # make user staff if in group dc-admin
            if user.groups.filter(name="dc-admin").exists():
                user.is_staff = True
                logger.info(f"Made {user.username} staff")

            user.save()

        except Exception as e:
            logger.error(
                (
                    "Could not populate user from CAS response ",
                    "(could be missing attributes): {}"
                ).format(str(e))
            )
            logger.debug(attributes)

        results = cas_user_set_up.send_robust(
            apps.get_model(app_label="dc_auth", model_name="profile"),
            user=user,
        )
        for req, resp in results:
            if isinstance(resp, Exception):
                logger.exception(resp)
