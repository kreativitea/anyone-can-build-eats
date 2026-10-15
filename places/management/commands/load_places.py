"""python manage.py load_places — add the places in data/places.json to the database.

Each place is found by its osm_id, so running it twice changes nothing, and running it
on a newer snapshot updates the places and keeps their reviews.
"""

import json
import math
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from places.models import Place

# The centre of the Nakamiya campus outline in OpenStreetMap (way 671222711).
NAKAMIYA = (34.8238967, 135.6649096)


def km_between(lat, lon, centre=NAKAMIYA):
    """Straight-line distance in km. Flat-earth maths is close enough within 5 km."""
    clat, clon = centre
    dy = (lat - clat) * 111.32
    dx = (lon - clon) * 111.32 * math.cos(math.radians(clat))
    return math.hypot(dx, dy)


class Command(BaseCommand):
    help = "Load the places from data/places.json (safe to run again)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", default=Path(settings.BASE_DIR) / "data" / "places.json"
        )

    def handle(self, *args, **options):
        snapshot = json.loads(Path(options["file"]).read_text(encoding="utf-8"))
        added = updated = 0
        with transaction.atomic():
            for row in snapshot["places"]:
                _, created = Place.objects.update_or_create(
                    osm_id=row["osm"],
                    defaults={
                        "name": row["name"],
                        "name_en": row.get("name_en", ""),
                        "category": row["category"],
                        "cuisine": row.get("cuisine", ""),
                        "opening_hours": row.get("opening_hours", ""),
                        "brand": row.get("brand", ""),
                        "lat": row["lat"],
                        "lon": row["lon"],
                        "km_from_campus": round(km_between(row["lat"], row["lon"]), 3),
                    },
                )
                added += created
                updated += not created
        self.stdout.write(
            f"{added} places added, {updated} updated. {snapshot['attribution']}."
        )
