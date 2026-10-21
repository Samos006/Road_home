import re

from django import forms

from .phones import PHONE_REGEX
from users.models import User


def validate_phone(phone: str, current_user_pk=None):
    if not phone:
        return phone

    if not re.match(PHONE_REGEX, phone):
        raise forms.ValidationError(
            "Номер должен начинаться с 8 или +7 и содержать ровно 10 цифр после кода"
        )
    
    if phone.startswith("8"):
        phone = "+7" + phone[1:]

    users_with_same_phone = User.objects.filter(phone=phone)

    if current_user_pk:
        users_with_same_phone = users_with_same_phone.exclude(pk=current_user_pk)

    if users_with_same_phone.exists():
        raise forms.ValidationError("Этот номер телефона уже используется")

    return phone
