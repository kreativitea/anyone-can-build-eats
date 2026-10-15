from django.test import TestCase

from places.tests.helpers import card_names, make_place


class PlaceListTests(TestCase):
    def test_nearest_first_twenty_to_a_page(self):
        for km in range(25, 0, -1):  # made in the wrong order on purpose
            make_place(name_en=f"Place {km}", km=km)
        response = self.client.get("/")
        self.assertEqual(card_names(response), [f"Place {km}" for km in range(1, 21)])
        second = self.client.get("/", {"page": 2})
        self.assertEqual(card_names(second), [f"Place {km}" for km in range(21, 26)])

    def test_bars_and_pubs_are_hidden_until_turned_on(self):
        make_place(name_en="Example Cafe", category="cafe")
        make_place(name_en="Example Bar", category="bar")
        make_place(name_en="Example Pub", category="pub")
        self.assertEqual(card_names(self.client.get("/")), ["Example Cafe"])
        shown = card_names(self.client.get("/", {"bars": "1"}))
        self.assertEqual(sorted(shown), ["Example Bar", "Example Cafe", "Example Pub"])

    def test_search_finds_a_place_by_either_name(self):
        make_place(name="例コーヒー", name_en="Example Coffee")
        make_place(name="例ラーメン", name_en="Example Ramen")
        self.assertEqual(
            card_names(self.client.get("/", {"q": "coffee"})), ["Example Coffee"]
        )
        self.assertEqual(
            card_names(self.client.get("/", {"q": "コーヒー"})), ["Example Coffee"]
        )

    def test_category_filter(self):
        make_place(name_en="Example Cafe", category="cafe")
        make_place(name_en="Example Ramen", category="restaurant")
        self.assertEqual(
            card_names(self.client.get("/", {"category": "cafe"})), ["Example Cafe"]
        )

    def test_htmx_gets_only_the_list(self):
        make_place(name_en="Example Ramen")
        full = self.client.get("/")
        part = self.client.get("/", HTTP_HX_REQUEST="true")
        self.assertContains(full, "<html")
        self.assertNotContains(part, "<html")
        self.assertContains(part, 'id="browse"')
        self.assertEqual(card_names(part), ["Example Ramen"])

    def test_every_page_credits_openstreetmap(self):
        self.assertContains(self.client.get("/"), "OpenStreetMap contributors")
