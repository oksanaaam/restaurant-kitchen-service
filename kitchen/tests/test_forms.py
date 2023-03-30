from django.test import TestCase

from kitchen.forms import CookCreationForm, CookExperienceUpdateForm, DishTypeSearchForm


class FormsTests(TestCase):
    def test_cook_driver_creation_form_with_years_of_experience_is_valid(self):
        form_data = {
            "username": "Marichka",
            "password1": "z54bvFG543",
            "password2": "z54bvFG543",
            "first_name": "Maria",
            "last_name": "Clinton",
            "email": "maria@gmail.com",
            "years_of_experience": 5
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_years_of_experience(self):
        form_data = {"years_of_experience": 6}
        form = CookExperienceUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_valid_search_dish_type_by_name(self):
        form_data = {"name": "Pasta"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
