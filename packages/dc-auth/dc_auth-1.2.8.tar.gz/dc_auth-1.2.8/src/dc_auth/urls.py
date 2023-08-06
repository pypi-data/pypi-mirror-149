from django.conf import settings
from django.urls import path, re_path
from django.views.generic.base import RedirectView

import django_cas_ng.views


def static(path):
    return RedirectView.as_view(
        url=settings.DC_STATIC_URL + path
    )


urlpatterns = [
    # -- Favicons and app icons --
    # keep favicon urls at root, but redirect to the favicon folder
    re_path(r"^favicon\.ico$", static("img/favicon/favicon.ico")),
    re_path(r"^favicon-32x32\.png$", static("img/favicon/favicon-32x32.png")),
    re_path(r"^favicon-16x16\.png$", static("img/favicon/favicon-16x16.png")),
    re_path(r"^manifest\.json$", static("img/favicon/manifest.json")),
    re_path(
        r"^safari-pinned-tab\.svg$",
        static("img/favicon/safari-pinned-tab.svg"),
    ),
    re_path(
        r"^android-chrome-192x192\.png$",
        static("img/favicon/android-chrome-192x192.png"),
    ),
    re_path(
        r"^android-chrome-512x512\.png$",
        static("img/favicon/android-chrome-512x512"),
    ),
    re_path(
        r"^apple-touch-icon\.png", static("img/favicon/apple-touch-icon.png"),
    ),
    re_path(
        r"^browserconfig\.xml",
        static("dc_auth/img/favicon/browserconfig.xml"),
    ),
    re_path(
        r"^mstile-150x150\.png",
        static("dc_auth/img/favicon/mstile-150x150.png"),
    ),
    path(
        "accounts/login/",
        django_cas_ng.views.LoginView.as_view(),
        name="cas_ng_login",
    ),
    path(
        "accounts/logout/",
        django_cas_ng.views.LogoutView.as_view(),
        name="cas_ng_logout",
    ),
    path(
        "accounts/callback/",
        django_cas_ng.views.CallbackView.as_view(),
        name="cas_ng_proxy_callback",
    ),
]
