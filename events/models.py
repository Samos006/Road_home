from django.db import models
from constants.events import *

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    description = models.TextField(verbose_name="Описание")

    urgency = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES,
        verbose_name="Срочность"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Статус"
    )

    place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место / адрес"
    )

    required_help = models.CharField(
        max_length=20,
        choices=HELP_CHOICES,
        blank=True,
        verbose_name="Что требуется"
    )

    start_date = models.DateField(
        verbose_name="Дата начала"
    )

    end_date = models.DateField(
        verbose_name="Дата окончания"
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="events"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "События"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title

class Application(models.Model):
    title = models.CharField(
        max_length=30,
        choices=APPLIC_TYPE,
        blank=False,
        verbose_name="Заявка"
    )
    
    animal = models.ForeignKey(
        "animals.Animal",
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Животное"
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Телефон",
    )

    telegram = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Telegram",
    )

    vk = models.URLField(
        blank=True,
        verbose_name="VK",
    )

    description = models.TextField(
        verbose_name="Описание"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
