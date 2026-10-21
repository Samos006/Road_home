import io
import random
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models

from constants.avatars import AVATAR_SIZE, BBOX, COLORS, FONT_SIZE, WHITE
from constants.users import UserFieldLength

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True
    )
    ROLE_CHOICES = [
        ("user", "Население"),
        ("shelter", "Приют"),
    ]    
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=UserFieldLength.NAME,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=UserFieldLength.SURNAME,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватарка",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )    
    phone = models.CharField(
        unique=True,
        max_length=UserFieldLength.PHONE,
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    vk = models.URLField(
        blank=True,
        verbose_name="Ссылка VK",
    )
    telegram = models.CharField(
        max_length=33,
        blank=True,
        verbose_name="Telegram",
    )
    about = models.TextField(
        blank=True,
        null=True,
        verbose_name="О себе",
    )
    favorites = models.ManyToManyField(
        "animals.Animal",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные животные",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "surname"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        size = AVATAR_SIZE
        color = random.choice(COLORS)
        letter = self.name[0].upper() if self.name else self.email[0].upper()

        img = Image.new("RGB", (size, size), color)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)

        bbox = draw.textbbox(BBOX, letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (size - w) / 2 - bbox[0]
        y = (size - h) / 2 - bbox[1]
        draw.text((x, y), letter, fill=WHITE, font=font)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        self.avatar.save(
            f"avatar_{uuid4()}.png", ContentFile(buffer.getvalue()), save=False
        )

