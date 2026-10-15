from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme


def safe_next(request):
    """Where to go after signing up: the page the person came from, if it is on this
    site. Anything else (another website) is ignored, so a link cannot send a new
    user somewhere harmful."""
    target = request.POST.get("next") or request.GET.get("next") or ""
    if url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return target
    return "places:list"


def signup(request):
    if request.user.is_authenticated:
        return redirect("places:list")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(
            request, f"Welcome, {user.username}. You can write reviews now."
        )
        return redirect(safe_next(request))
    return render(
        request,
        "registration/signup.html",
        {"form": form, "next": request.GET.get("next", "")},
    )
