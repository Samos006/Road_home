from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from constants.validators import validate_phone
from users.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )   
    confirm_password = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ["username", "name", "surname", "role"]
    
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data
    
    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class UserEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    
    class Meta:
        model = User
        fields = ["name", "surname", "phone", "email", "vk", "telegram", "about", "avatar"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        return validate_phone(phone, current_user_pk=self.instance.pk)



class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")
