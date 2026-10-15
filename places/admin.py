from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "name_en", "category", "cuisine", "km_from_campus"]
    list_filter = ["category"]
    search_fields = ["name", "name_en", "cuisine", "osm_id"]
