from django.conf import settings
from django.db import models
from constants.animals import *


class Animal(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Кличка",
    )

    age = models.PositiveIntegerField(
        verbose_name="Возраст",
    )

    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        verbose_name="Пол",
    )

    animal_type = models.CharField(
        max_length=10,
        choices=ANIMAL_TYPE_CHOICES,
        verbose_name="Тип животного",
    )

    color = models.CharField(
        max_length=30,
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
        verbose_name="Окрас",
    )

    character = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Характер",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="animals",
        verbose_name="Владелец",
    )

    vaccine = models.BooleanField(
        default=False,
        verbose_name="Вакцинация",
    )

    castration = models.BooleanField(
        default=False,
        verbose_name="Кастрация",
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="searching",
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def age_display(self):
        months = self.age

        if months < 12:
            if months % 10 == 1 and months != 11:
                return f"{months} месяц"
            elif months % 10 in (2, 3, 4) and months not in (12, 13, 14):
                return f"{months} месяца"
            else:
                return f"{months} месяцев"

        years = months / 12

        if years.is_integer():
            years = int(years)
        else:
            years = round(years, 1)

        if years == 1:
            return "1 год"
        elif years == 1.5:
            return "1.5 года"
        elif years % 10 == 1 and years != 11:
            return f"{years} год"
        elif years % 10 in (2, 3, 4) and years not in (12, 13, 14):
            return f"{years} года"
        else:
            return f"{years} лет"
                
    class Meta:
        verbose_name = "животное"
        verbose_name_plural = "Животные"

    def __str__(self):
        return f"{self.id} — {self.name}"


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    image = models.ImageField(
        upload_to="animals/",
        verbose_name="Фото",
    )

    class Meta:
        verbose_name = "фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото {self.animal.name}"
