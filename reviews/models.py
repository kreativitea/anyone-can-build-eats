from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from places.models import Place

TEXT_LIMIT = 2000


class Review(models.Model):
    class Stars(models.IntegerChoices):
        ONE = 1, "1 star"
        TWO = 2, "2 stars"
        THREE = 3, "3 stars"
        FOUR = 4, "4 stars"
        FIVE = 5, "5 stars"

    # Deleting a place deletes its reviews; so does deleting a user.
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="reviews")
    # Always the person logged in, set by the view. Never a field in a form.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        choices=Stars.choices,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField(max_length=TEXT_LIMIT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return f"{self.author} on {self.place}: {self.rating}"
