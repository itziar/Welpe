from __future__ import unicode_literals

from django.conf.urls import url

from Welpe.manageUser import views
from mezzanine.conf import settings


ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))
SIGNUP_VERIFY_URL = getattr(settings, "SIGNUP_VERIFY_URL",
                            "/%s/verify/" % ACCOUNT_URL.strip("/"))
LOGIN_URL = getattr(settings, "LOGIN_URL", "/login")
LOGOUT_URL = getattr(settings, "LOGOUT_URL", "/logout/")
PROFILE_URL = getattr(settings, "PROFILE_URL", "/users/")
PROFILE_UPDATE_URL = getattr(settings, "PROFILE_UPDATE_URL",
                             "/%s/update/" % ACCOUNT_URL.strip("/"))
PASSWORD_RESET_URL = getattr(settings, "PASSWORD_RESET_URL",
                             "/%s/password/reset/" % ACCOUNT_URL.strip("/"))
PASSWORD_RESET_VERIFY_URL = getattr(settings, "PASSWORD_RESET_VERIFY_URL",
                                    "/%s/password/verify/" %
                                    ACCOUNT_URL.strip("/"))

_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"
_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^%s%s$" % (LOGIN_URL.strip("/"), _slash),
        views.login, name="login"),

    url("^%s%s$" % (LOGOUT_URL.strip("/"), _slash),
        views.logout, name="logout"),
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
        views.signup, name="signup"),
    url("^%s%s%s$" % (SIGNUP_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        views.signup_verify, name="signup_verify"),
    url("^%s%s$" % (PROFILE_UPDATE_URL.strip("/"), _slash),
        views.profile_update, name="profile_update"),
    url("^%s%s$" % (PASSWORD_RESET_URL.strip("/"), _slash),
        views.password_reset, name="mezzanine_password_reset"),
    url("^%s%s%s$" %
        (PASSWORD_RESET_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        views.password_reset_verify, name="password_reset_verify"),
    url("^%s%s$" % (ACCOUNT_URL.strip("/"), _slash),
        views.account_redirect, name="account_redirect"),
]

