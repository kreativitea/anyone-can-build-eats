from django.urls import path

from . import views

app_name = "reviews"
urlpatterns = [
    path("places/<int:place_pk>/review/", views.review_create, name="create"),
]
