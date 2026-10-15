import json
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from places.management.commands.load_places import km_between
from places.models import Place

SNAPSHOT = {
    "attribution": "© OpenStreetMap contributors",
    "places": [
        {
            "osm": "node/1",
            "category": "cafe",
            "lat": 34.8236441,
            "lon": 135.6635768,
            "name": "例カフェ",
            "name_en": "Example Cafe",
        },
        {
            "osm": "way/2",
            "category": "bar",
            "lat": 34.83,
            "lon": 135.67,
            "name": "例バー",
        },
    ],
}


class LoadPlacesTests(TestCase):
    def load(self, snapshot):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "places.json"
            path.write_text(json.dumps(snapshot), encoding="utf-8")
            call_command("load_places", file=path, stdout=StringIO())

    def test_loads_every_place_with_its_distance(self):
        self.load(SNAPSHOT)
        self.assertEqual(Place.objects.count(), 2)
        cafe = Place.objects.get(osm_id="node/1")
        self.assertEqual(cafe.name_en, "Example Cafe")
        self.assertAlmostEqual(cafe.km_from_campus, 0.125, places=3)

    def test_loading_twice_changes_nothing(self):
        self.load(SNAPSHOT)
        self.load(SNAPSHOT)
        self.assertEqual(Place.objects.count(), 2)

    def test_a_newer_snapshot_updates_the_place(self):
        self.load(SNAPSHOT)
        newer = json.loads(json.dumps(SNAPSHOT))
        newer["places"][0]["name_en"] = "Example Cafe Renamed"
        self.load(newer)
        self.assertEqual(
            Place.objects.get(osm_id="node/1").name_en, "Example Cafe Renamed"
        )

    def test_distance_from_campus_to_itself_is_zero(self):
        self.assertEqual(km_between(34.8238967, 135.6649096), 0)
