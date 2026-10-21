from django.contrib import admin
from .models import Event, Application


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "urgency",
        "status",
        "required_help",
        "start_date",
        "end_date",
        "owner",
        "created_at",
    )

    list_filter = (
        "urgency",
        "status",
        "required_help",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "place",
        "owner__username",
        "owner__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("title", "animal", "owner", "phone", "telegram", "created_at")
    list_filter = ("title", "created_at")
    search_fields = ("owner__username", "owner__name", "animal__name", "phone", "telegram")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
 
    fieldsets = (
        ("Основное", {
            "fields": ("title", "animal", "owner")
        }),
        ("Контакты", {
            "fields": ("phone", "telegram", "vk")
        }),
        ("Описание", {
            "fields": ("description",)
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at"),
        }),
    )