from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.views import signup

urlpatterns = [
    path("admin/", admin.site.urls),
    # Accounts. Not include("django.contrib.auth.urls"): that also adds the
    # password-reset pages, which need email.
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", signup, name="signup"),
    path("", include("reviews.urls")),
    path("", include("places.urls")),
]
