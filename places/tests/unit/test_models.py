from django.test import TestCase

from places.models import Place
from places.tests.helpers import make_place


class NameTests(TestCase):
    def test_english_name_first_and_sign_name_under_it(self):
        place = make_place(name="例ラーメン", name_en="Example Ramen")
        self.assertEqual(place.display_name, "Example Ramen")
        self.assertEqual(place.local_name, "例ラーメン")

    def test_no_english_name_shows_the_sign_name_once(self):
        place = make_place(name="例の定食屋", name_en="")
        self.assertEqual(place.display_name, "例の定食屋")
        self.assertEqual(place.local_name, "")

    def test_cuisine_reads_as_words(self):
        place = make_place(cuisine="noodle;coffee_shop")
        self.assertEqual(place.cuisine_label, "noodle, coffee shop")


class RatingTests(TestCase):
    def test_a_place_with_no_reviews_has_no_rating(self):
        make_place()
        place = Place.objects.with_ratings().get()
        self.assertIsNone(place.rating)
        self.assertEqual(place.review_count, 0)
