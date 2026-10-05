from django import forms
from django.contrib.auth.models import User

from .models import Game
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Ім'я користувача",
            "password1": "Пароль",
            "password2": "Підтвердження пароля",
        }
        help_texts = {
            "username": "До 150 символів. Лише літери, цифри та @/./+/-/_.",
            "password1": "Пароль має бути достатньо надійним.",
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Ім'я адміністратора")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            "title", "description", "price", "old_price", "image", "image_url",
            "steam_app_id", "is_popular", "is_indie", "is_aaa", "is_free_to_play",
            "price_currency", "developer", "publisher", "genre", "release_date",
        )
        labels = {
            "title": "Назва гри",
            "description": "Опис",
            "price": "Ціна",
            "old_price": "Стара ціна",
            "image": "Локальне зображення",
            "image_url": "URL зображення",
            "steam_app_id": "Steam App ID",
            "is_popular": "Популярна",
            "is_indie": "Інді",
            "is_aaa": "AAA",
            "is_free_to_play": "Безкоштовна",
            "price_currency": "Валюта",
            "developer": "Розробник",
            "publisher": "Видавець",
            "genre": "Жанр",
            "release_date": "Дата виходу",
        }
        help_texts = {
            "image": "Необов'язково, якщо вказано URL зображення.",
            "image_url": "Можна вставити пряме посилання на обкладинку.",
            "steam_app_id": "Необов'язково. Для Steam-обкладинки вкажіть ID гри.",
        }

    def clean(self):
        cleaned = super().clean()
        title = cleaned.get("title")
        image = cleaned.get("image")
        image_url = cleaned.get("image_url")
        steam_id = cleaned.get("steam_app_id")

        if not image and not image_url and not steam_id:
            self.add_error(
                "image_url",
                "Вкажіть URL зображення, Steam App ID або завантажте файл."
            )

        if title:
            cleaned["title"] = title.strip()

        return cleaned
