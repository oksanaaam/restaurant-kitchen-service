from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish


class ModelsTests(TestCase):
    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="Johnie",
            password="RE0v4Q4n",
            first_name="John",
            last_name="Smith"
        )
        self.assertEqual(
            str(cook),
            (f"{cook.username}, email: {cook.email}, "
             f"years of experience: {cook.years_of_experience}")
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(
            name="Soup",
        )
        dish = Dish.objects.create(
            name="Tomato",
            dish_type=dish_type,
            price=100
        )
        self.assertEqual(str(dish), f"{dish.name}, dish_type: {dish.dish_type}, price: {dish.price}")

    def test_create_cook_with_years_of_experience(self):
        username = "Den"
        password = "12345"
        years_of_experience = 2
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )
        self.assertEqual(cook.username, username)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.years_of_experience, years_of_experience)
