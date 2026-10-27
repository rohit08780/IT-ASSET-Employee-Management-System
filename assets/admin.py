
from django.contrib import admin
from .models import Asset

# Register your models here.
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_tag",
        "asset_name",
        "category",
        "brand",
        "status",
        "assigned_to",
        "purchase_date",
    )

    list_filter = ("category", "status", "brand")
    search_fields = ("asset_tag", "asset_name", "brand", "serial_number")
    ordering = ("asset_tag",)