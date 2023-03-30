from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook

COOK_URL = reverse("kitchen:cook-list")
DISH_TYPE_URL = reverse("kitchen:dish-type-list")
DISH_URL = reverse("kitchen:dish-list")
DISH_CREATE_URL = reverse("kitchen:dish-create")


class PublicCookTest(TestCase):
    def test_login_required(self):
        res = self.client.get(COOK_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            "admin",
            "admin123"
        )
        self.client.force_login(self.cook)

    def test_retrieve_cook(self):
        Cook.objects.create(
            username="John",
            password="12345",
            years_of_experience=1
        )
        Cook.objects.create(
            username="Lina",
            password="123456",
            years_of_experience=3
        )
        response = self.client.get(COOK_URL)
        cooks = Cook.objects.filter(username__icontains="n")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks)
        )
        self.assertTemplateUsed(response, "kitchen/cook_list.html")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = get_user_model().objects.create_user(
            "David",
            "David9999"
        )
        self.client.force_login(self.dish_type)

    def test_retrieve_dish_type(self):
        DishType.objects.create(
            name="Pasta"
        )
        DishType.objects.create(
            name="Pizza"
        )
        response = self.client.get(DISH_TYPE_URL)
        dish_types = DishType.objects.filter(name__icontains="p")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_types_list"]),
            list(dish_types)
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_dishes_create(self):
        response = self.client.get(DISH_CREATE_URL)

        self.assertEqual(response.status_code, 200)


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.dish = get_user_model().objects.create_user(
            "Stepan",
            "asdf43eewqd3Q"
        )
        self.client.force_login(self.dish)

    def test_retrieve_dish(self):
        dish_type = DishType.objects.create(
            name="Pizza"
        )
        Dish.objects.create(
            name="Pepperoni",
            price=130,
            dish_type=dish_type
        )
        Dish.objects.create(
            name="Margherita",
            price=110,
            dish_type=dish_type
        )
        response = self.client.get(DISH_URL)
        dishes = Dish.objects.filter(name__icontains="i")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes)
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")
