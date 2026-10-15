from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from places.models import Place

from .forms import ReviewForm


@login_required
def review_create(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.place = place
        review.author = request.user  # always the person logged in
        review.save()
        messages.success(request, "Your review is saved.")
        return redirect("places:detail", pk=place.pk)
    # A first visit, or a form with a mistake: show it, with what was typed kept.
    status = 400 if request.method == "POST" else 200
    return render(
        request, "reviews/form.html", {"form": form, "place": place}, status=status
    )
