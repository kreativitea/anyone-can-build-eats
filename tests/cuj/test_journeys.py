"""Whole journeys a person takes, through Django's test client, with CSRF checks on,
the way a browser would: each step uses what the page before it showed."""

import re

from django.test import Client, TestCase

from places.tests.helpers import TEST_PASSWORD, make_place


def csrf_token(response):
    return re.search(
        r'name="csrfmiddlewaretoken" value="([^"]+)"', response.content.decode()
    )[1]


class VisitorJourneyTests(TestCase):
    def test_a_visitor_searches_and_opens_a_place(self):
        place = make_place(name="例そば", name_en="Example Soba")
        make_place(name="例カレー", name_en="Example Curry")
        client = Client(enforce_csrf_checks=True)
        results = client.get("/", {"q": "soba"})
        self.assertContains(results, "Example Soba")
        self.assertNotContains(results, "Example Curry")
        self.assertContains(results, f'href="/places/{place.pk}/"')
        page = client.get(f"/places/{place.pk}/")
        self.assertContains(page, "例そば")
        self.assertContains(page, "Write a review")


class NewReviewerJourneyTests(TestCase):
    def test_a_new_person_signs_up_and_writes_a_review(self):
        place = make_place(name_en="Example Soba")
        review_url = f"/places/{place.pk}/review/"
        client = Client(enforce_csrf_checks=True)

        # Write a review → sent to log in → no account yet, so sign up.
        login = client.get(review_url, follow=True)
        self.assertContains(login, "Log in")
        signup = client.get(f"/accounts/signup/?next={review_url}")
        form = client.post(
            "/accounts/signup/",
            {
                "username": "ana",
                "password1": TEST_PASSWORD,
                "password2": TEST_PASSWORD,
                "next": review_url,
                "csrfmiddlewaretoken": csrf_token(signup),
            },
            follow=True,
        )
        self.assertContains(form, "Write a review")

        saved = client.post(
            review_url,
            {
                "rating": 5,
                "text": "Quick and kind.",
                "csrfmiddlewaretoken": csrf_token(form),
            },
            follow=True,
        )
        self.assertContains(saved, "Your review is saved.")
        self.assertContains(saved, "Quick and kind.")
        self.assertContains(saved, "1 review")
