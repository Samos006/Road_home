from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "avatar_preview",
        "username",
        "email",
        "name",
        "surname",
        "role",
        "phone",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "name",
        "surname",
        "phone",
    )

    ordering = ("-date_joined",)

    readonly_fields = (
        "avatar_preview",
        "date_joined",
        "last_login",
    )

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "username",
                "password",
                "email",
                "name",
                "surname",
                "role",
            )
        }),

        ("Аватар и описание", {
            "fields": (
                "avatar",
                "avatar_preview",
                "about",
            )
        }),

        ("Контакты", {
            "fields": (
                "phone",
                "telegram",
                "vk",
            )
        }),

        ("Избранное", {
            "fields": (
                "favorites",
            )
        }),

        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Даты", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        ("Создание пользователя", {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "name",
                "surname",
                "role",
                "password1",
                "password2",
            ),
        }),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
        "favorites",
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="border-radius:50%; object-fit:cover;" />',
                obj.avatar.url
            )
        return "Нет аватара"

    avatar_preview.short_description = "Аватар"