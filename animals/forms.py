from django import forms
from animals.models import Animal
from constants.animals import CHARACTER_CHOICES


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        return files.getlist(name)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def to_python(self, data):
        if data in self.empty_values:
            return []
        return [super(MultipleFileField, self).to_python(f) for f in data]


class AnimalForm(forms.ModelForm):
    character = forms.MultipleChoiceField(
        choices=CHARACTER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    photos = MultipleFileField(
        required=False,
        label="Фотографии",
    )

    class Meta:
        model = Animal
        fields = [
            "name", "age", "sex", "animal_type", "color",
            "character", "description", "vaccine", "status", "castration",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Описание животного",
            }),
        }

    def clean_photos(self):
        photos = self.cleaned_data.get("photos", [])
        if len(photos) > 5:
            raise forms.ValidationError("Можно загрузить максимум 5 фотографий")
        return photos

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 0:
            raise forms.ValidationError("Возраст не может быть отрицательным")
        return age


class AnimalEditForm(AnimalForm):
    pass