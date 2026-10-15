from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.cache import patch_vary_headers
from django.utils.http import urlencode

from .models import NIGHTLIFE, Place

PAGE_SIZE = 20
SEARCH_MAX_LENGTH = 100


def wants_partial(request):
    """True when htmx asked for just the list, not the whole page.

    htmx sends HX-Request on every request it makes. When the reader presses Back,
    htmx may ask for the page again to restore it, with HX-History-Restore-Request:
    that one needs the whole page.
    """
    return (
        request.headers.get("HX-Request") == "true"
        and request.headers.get("HX-History-Restore-Request") != "true"
    )


def place_list(request):
    q = request.GET.get("q", "").strip()[:SEARCH_MAX_LENGTH]
    bars = request.GET.get("bars") == "1"
    category = request.GET.get("category", "")
    categories = [
        (value, label)
        for value, label in Place.Category.choices
        if bars or value not in NIGHTLIFE
    ]
    if category not in dict(categories):
        category = ""

    places = Place.objects.with_ratings()
    if not bars:
        places = places.daytime()
    if category:
        places = places.filter(category=category)
    if q:
        places = places.filter(Q(name__icontains=q) | Q(name_en__icontains=q))

    # Said again here, on purpose: Django drops a model's default ordering from a
    # query that works out an average (with_ratings), so it would come out by id.
    places = places.order_by("km_from_campus", "pk")
    page = Paginator(places, PAGE_SIZE).get_page(request.GET.get("page"))
    # The filters as they are now, for the page links, so a new page keeps them.
    kept = {key: value for key, value in [("q", q), ("category", category)] if value}
    if bars:
        kept["bars"] = "1"

    context = {
        "page": page,
        "q": q,
        "bars": bars,
        "category": category,
        "categories": categories,
        "kept_query": urlencode(kept),
        "search_max_length": SEARCH_MAX_LENGTH,
    }
    template = "places/_browse.html" if wants_partial(request) else "places/list.html"
    response = render(request, template, context)
    # The same address sends two different answers, so caches must tell them apart.
    patch_vary_headers(response, ["HX-Request"])
    return response


def place_detail(request, pk):
    place = get_object_or_404(Place.objects.with_ratings(), pk=pk)
    reviews = place.reviews.select_related("author").order_by("-created_at", "-pk")
    return render(request, "places/detail.html", {"place": place, "reviews": reviews})
