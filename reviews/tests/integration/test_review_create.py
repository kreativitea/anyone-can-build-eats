from django.test import TestCase

from places.models import Place
from places.tests.helpers import make_place, make_user
from reviews.models import Review


class WriteReviewTests(TestCase):
    def setUp(self):
        self.place = make_place()
        self.url = f"/places/{self.place.pk}/review/"
        self.ana = make_user("ana")

    def post(self, **data):
        return self.client.post(self.url, {"rating": 4, "text": "Good soup.", **data})

    def test_a_saved_review_comes_first_and_changes_the_rating(self):
        self.client.force_login(self.ana)
        self.post(text="First visit.")
        response = self.post(rating=5, text="Second visit.")
        self.assertRedirects(
            response, f"/places/{self.place.pk}/", fetch_redirect_response=False
        )
        page = self.client.get(f"/places/{self.place.pk}/")
        reviews = list(page.context["reviews"])
        self.assertEqual([r.text for r in reviews], ["Second visit.", "First visit."])
        self.assertContains(page, "2 reviews")
        self.assertContains(page, "Your review is saved.")

    def test_rating_is_the_average_to_one_decimal(self):
        self.client.force_login(self.ana)
        for stars in [4, 4, 5]:
            self.post(rating=stars)
        place = Place.objects.with_ratings().get(pk=self.place.pk)
        self.assertAlmostEqual(place.rating, 13 / 3)
        self.assertContains(self.client.get(f"/places/{self.place.pk}/"), "4.3")

    def test_a_rating_outside_one_to_five_is_refused(self):
        self.client.force_login(self.ana)
        for bad in [0, 6, "great", ""]:
            with self.subTest(rating=bad):
                response = self.post(rating=bad)
                self.assertContains(
                    response, "Choose from 1 to 5 stars.", status_code=400
                )
        self.assertEqual(Review.objects.count(), 0)

    def test_an_empty_review_is_refused_and_the_stars_are_kept(self):
        self.client.force_login(self.ana)
        response = self.post(rating=3, text="   ")
        self.assertContains(
            response, "Write something about the place.", status_code=400
        )
        self.assertContains(response, 'value="3" checked', status_code=400)
        self.assertEqual(Review.objects.count(), 0)

    def test_a_visitor_is_sent_to_log_in_and_nothing_is_saved(self):
        for response in [self.client.get(self.url), self.post()]:
            self.assertRedirects(
                response,
                f"/accounts/login/?next={self.url}",
                fetch_redirect_response=False,
            )
        self.assertEqual(Review.objects.count(), 0)

    def test_the_author_is_always_the_person_logged_in(self):
        ben = make_user("ben")
        self.client.force_login(self.ana)
        self.post(author=ben.pk)
        self.assertEqual(Review.objects.get().author, self.ana)
