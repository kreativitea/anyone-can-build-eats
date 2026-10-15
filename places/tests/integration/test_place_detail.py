from django.test import TestCase

from places.tests.helpers import make_place


class PlaceDetailTests(TestCase):
    def test_shows_both_names_and_no_reviews_yet(self):
        place = make_place(name="例ラーメン", name_en="Example Ramen")
        response = self.client.get(f"/places/{place.pk}/")
        self.assertContains(response, "Example Ramen")
        self.assertContains(response, "例ラーメン")
        self.assertContains(response, "No reviews yet")
        self.assertContains(response, f"https://www.openstreetmap.org/{place.osm_id}")

    def test_unknown_place_is_404(self):
        self.assertEqual(self.client.get("/places/999999/").status_code, 404)
