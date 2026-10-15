from django.db import models
from django.db.models import Avg, Count

# Bars and pubs are hidden unless the reader turns them on.
NIGHTLIFE = ["bar", "pub"]


class PlaceQuerySet(models.QuerySet):
    def with_ratings(self):
        """Each place with its average rating and number of reviews.

        Worked out by the database every time, never stored, so it can never
        disagree with the reviews. A place with no reviews has rating None.
        """
        return self.annotate(
            rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )

    def daytime(self):
        """Every place except bars and pubs."""
        return self.exclude(category__in=NIGHTLIFE)


class Place(models.Model):
    class Category(models.TextChoices):
        RESTAURANT = "restaurant", "Restaurant"
        CAFE = "cafe", "Café"
        FAST_FOOD = "fast_food", "Fast food"
        ICE_CREAM = "ice_cream", "Ice cream"
        BAR = "bar", "Bar"
        PUB = "pub", "Pub"

    # Where the place is in OpenStreetMap, like "node/14146066463".
    osm_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)  # as on the sign, usually Japanese
    name_en = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    cuisine = models.CharField(max_length=100, blank=True)  # OSM's tag: "ramen"
    opening_hours = models.CharField(max_length=200, blank=True)  # OSM's format
    brand = models.CharField(max_length=100, blank=True)  # a chain's name
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lon = models.DecimalField(max_digits=10, decimal_places=7)
    # Straight-line distance from the Nakamiya campus, worked out by load_places.
    km_from_campus = models.FloatField()

    objects = PlaceQuerySet.as_manager()

    class Meta:
        ordering = ["km_from_campus", "pk"]

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        """The English name when there is one, else the name on the sign."""
        return self.name_en or self.name

    @property
    def local_name(self):
        """The name on the sign, shown under the English one. Empty if it adds nothing."""
        if self.name_en and self.name_en != self.name:
            return self.name
        return ""

    @property
    def cuisine_label(self):
        """OSM writes "noodle;ramen" or "coffee_shop"; people read "noodle, ramen"."""
        parts = [part.strip().replace("_", " ") for part in self.cuisine.split(";")]
        return ", ".join(part for part in parts if part)

    @property
    def osm_url(self):
        return f"https://www.openstreetmap.org/{self.osm_id}"
