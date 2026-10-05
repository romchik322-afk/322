from django.contrib import admin
from .models import Profile, Game, Library, Favorite, Cart


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title", "price", "price_currency", "discount_percent",
        "is_popular", "is_aaa", "is_indie", "is_free_to_play",
        "genre", "developer", "publisher", "release_date"
    )
    list_display_links = ("title",)
    search_fields = ("title", "developer", "publisher", "genre", "description")
    list_filter = ("genre", "is_popular", "is_aaa", "is_indie", "is_free_to_play", "price_currency")
    list_editable = ("price", "is_popular")
    date_hierarchy = "release_date"
    ordering = ("-created_at",)
    fieldsets = (
        ("Основна інформація", {
            "fields": ("title", "description", "image", "image_url")
        }),
        ("Ціна", {
            "fields": ("price", "old_price", "price_currency")
        }),
        ("Категорії", {
            "fields": ("is_popular", "is_indie", "is_aaa", "is_free_to_play", "genre")
        }),
        ("Дані гри", {
            "fields": ("steam_app_id", "developer", "publisher", "release_date")
        }),
        ("Steam", {
            "fields": ("price_updated_at",),
            "classes": ("collapse",)
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    search_fields = ("user__username", "user__email")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "added_at")
    search_fields = ("user__username", "game__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "game")
    search_fields = ("user__username", "game__title")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


admin.site.site_header = "NEVERSTORE — Адмін-панель"
admin.site.site_title = "NEVERSTORE Admin"
admin.site.index_title = "Керування магазином"
