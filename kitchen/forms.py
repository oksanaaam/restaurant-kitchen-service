from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Cook, Dish


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience"
        )

    def clean_years_of_experience(self) -> int:
        years_of_experience = self.cleaned_data["years_of_experience"]
        license_experience_validator(years_of_experience)
        return years_of_experience


def license_experience_validator(years_of_experience: int):
    if not isinstance(years_of_experience, int):
        raise ValidationError("Ensure experience must be an integer")
    if years_of_experience < 0:
        raise ValidationError("Ensure experience cannot be less than 0")


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience"
        )

    def clean_years_of_experience(self) -> int:
        years_of_experience = self.cleaned_data["years_of_experience"]
        license_experience_validator(years_of_experience)
        return years_of_experience


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."})
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )
