from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook

COOK_URL = reverse("kitchen:cook-list")
COOK_CREATE_URL = reverse("kitchen:cook-create")
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

    def test_update_cook(self):
        cook = Cook.objects.create(
            username="John",
            password="12345",
            years_of_experience=1
        )
        new_data = {
            "username": "Johnny",
            "password": "newpassword",
            "years_of_experience": 3
        }
        url = reverse("kitchen:cook-update", args=[cook.pk])
        response = self.client.post(url, new_data)
        self.assertEqual(response.status_code, 302)
        updated_cook = Cook.objects.get(pk=cook.pk)
        self.assertEqual(updated_cook.username, new_data["username"])
        self.assertEqual(updated_cook.years_of_experience, new_data["years_of_experience"])

    def test_delete_cook(self):
        cook = Cook.objects.create(
            username="Lina",
            password="123456",
            years_of_experience=3
        )
        url = reverse("kitchen:cook-delete", args=[cook.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cook.objects.filter(pk=cook.pk).exists())


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

    def test_create_dish_type(self):
        dish_type_count = DishType.objects.count()
        data = {"name": "Seafood"}
        response = self.client.post(reverse("kitchen:dish-type-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.count(), dish_type_count + 1)

    def test_update_dish_type(self):
        dish_type = DishType.objects.create(name="Cream")
        data = {"name": "Ice cream"}
        url = reverse("kitchen:dish-type-update", args=[dish_type.id])
        response = self.client.post(url, data)
        updated_dish_type = DishType.objects.get(id=dish_type.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_dish_type.name, "Ice cream")

    def test_delete_dish_type(self):
        dish_type = DishType.objects.create(name="Ice cream")
        url = reverse("kitchen:dish-type-delete", args=[dish_type.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(id=dish_type.id).exists())


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

    def test_dishes_create(self):
        response = self.client.get(DISH_CREATE_URL)

        self.assertEqual(response.status_code, 200)

    def test_delete_dish(self):
        dish_type = DishType.objects.create(
            name="Salad"
        )
        dish = Dish.objects.create(
            name="Caesar Salad",
            price=120,
            dish_type=dish_type
        )
        url = reverse("kitchen:dish-delete", args=[dish.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(pk=dish.pk).exists())
