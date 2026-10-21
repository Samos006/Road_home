from django.contrib import admin
from django.utils.html import format_html

from .models import Animal, AnimalPhoto


class AnimalPhotoInline(admin.TabularInline):
    model = AnimalPhoto
    extra = 1

    readonly_fields = ("preview",)

    fields = (
        "image",
        "preview",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" style="border-radius:10px;" />',
                obj.image.url
            )
        return "Нет фото"

    preview.short_description = "Превью"


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "animal_type",
        "sex",
        "age_display",
        "status",
        "vaccine",
        "castration",
        "owner",
        "created_at",
    )

    list_filter = (
        "animal_type",
        "sex",
        "status",
        "vaccine",
        "castration",
        "color",
    )

    search_fields = (
        "name",
        "description",
        "owner__username",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [AnimalPhotoInline]

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "name",
                "age",
                "sex",
                "animal_type",
                "color",
                "status",
            )
        }),

        ("Описание", {
            "fields": (
                "character",
                "description",
            )
        }),

        ("Медицинская информация", {
            "fields": (
                "vaccine",
                "castration",
            )
        }),

        ("Владелец", {
            "fields": (
                "owner",
            )
        }),

        ("Системная информация", {
            "fields": (
                "created_at",
            )
        }),
    )


@admin.register(AnimalPhoto)
class AnimalPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "animal",
        "preview",
    )

    readonly_fields = (
        "preview",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px;" />',
                obj.image.url
            )
        return "Нет фото"

    preview.short_description = "Фото"