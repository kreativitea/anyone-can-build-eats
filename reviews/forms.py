from django import forms

from .models import TEXT_LIMIT, Review


class ReviewForm(forms.ModelForm):
    """The stars and the text. The place and the author come from the view, never
    from the form, so nobody can post a review as someone else."""

    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {"rating": forms.RadioSelect}
        labels = {"rating": "Your rating", "text": "Your review"}
        help_texts = {"text": f"At most {TEXT_LIMIT:,} characters."}
        error_messages = {
            "rating": {
                "required": "Choose from 1 to 5 stars.",
                "invalid_choice": "Choose from 1 to 5 stars.",
            },
            "text": {
                "required": "Write something about the place.",
                "max_length": f"Keep it to {TEXT_LIMIT:,} characters.",
            },
        }
