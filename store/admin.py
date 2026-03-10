from django.contrib import admin
from django.utils.html import format_html

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("preview", "name", "flavor", "price", "stock", "is_active", "hero_product", "sort_order")
    list_editable = ("price", "stock", "is_active", "hero_product", "sort_order")
    list_filter = ("is_active", "hero_product")
    search_fields = ("name", "flavor", "slug")
    prepopulated_fields = {"slug": ("name",)}

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:8px;" />', obj.image.url)
        return "—"

    preview.short_description = "Превью"
