from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = "dc_auth"

    def ready(self):
        import dc_auth.signals  # noqa: F401
