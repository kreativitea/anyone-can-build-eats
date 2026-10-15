"""Helpers the tests share. Every place here is made up: the real places are real
businesses, and a test must never write a review of one."""

from django.contrib.auth import get_user_model

from places.models import Place

TEST_PASSWORD = "a-test-password-1234"  # a test value, only for these tests


def make_place(name="例ラーメン", name_en="Example Ramen", km=0.5, **fields):
    number = Place.objects.count() + 1
    defaults = {
        "osm_id": f"node/test-{number}",
        "category": Place.Category.RESTAURANT,
        "lat": "34.8200000",
        "lon": "135.6600000",
    }
    defaults.update(fields)
    return Place.objects.create(
        name=name, name_en=name_en, km_from_campus=km, **defaults
    )


def make_user(username="ana"):
    return get_user_model().objects.create_user(username, password=TEST_PASSWORD)


def card_names(response):
    """The names on the place cards, in order, as the page shows them."""
    return [place.display_name for place in response.context["page"]]
