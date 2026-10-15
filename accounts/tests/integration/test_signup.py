from django.contrib.auth import get_user_model
from django.test import TestCase

from places.tests.helpers import TEST_PASSWORD


class SignupTests(TestCase):
    def sign_up(self, next_url=""):
        return self.client.post(
            "/accounts/signup/",
            {
                "username": "ana",
                "password1": TEST_PASSWORD,
                "password2": TEST_PASSWORD,
                "next": next_url,
            },
        )

    def test_signing_up_logs_you_in(self):
        response = self.sign_up()
        self.assertRedirects(response, "/")
        self.assertTrue(get_user_model().objects.filter(username="ana").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_signing_up_goes_back_where_you_were(self):
        self.assertRedirects(
            self.sign_up("/places/1/review/"),
            "/places/1/review/",
            fetch_redirect_response=False,
        )

    def test_another_website_is_never_where_you_go(self):
        self.assertRedirects(self.sign_up("https://example.com/"), "/")
