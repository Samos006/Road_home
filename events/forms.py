from django import forms
from .models import Event, Application


class EventForm(forms.ModelForm):
    class Meta:
        model = Event

        fields = [
            "title",
            "description",
            "urgency",
            "status",
            "place",
            "required_help",
            "start_date",
            "end_date",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={
                "type": "date"
            }),

            "end_date": forms.DateInput(attrs={
                "type": "date"
            }),

            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Описание события"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError(
                "Дата окончания не может быть раньше даты начала"
            )

        return cleaned_data
    
class EventEditForm(EventForm):
    pass

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application

        fields = [
            "title",
            "phone",
            "telegram",
            "vk",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Описание заявки"
            }),
        }
    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone")
        telegram = cleaned_data.get("telegram")
        vk = cleaned_data.get("vk")
        
        if not phone and not telegram and not vk:
            raise forms.ValidationError(
                "Укажите хотя бы один способ связи"
            )

        return cleaned_data