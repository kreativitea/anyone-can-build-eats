from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["place", "author", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["text", "author__username", "place__name", "place__name_en"]
    raw_id_fields = ["place"]
