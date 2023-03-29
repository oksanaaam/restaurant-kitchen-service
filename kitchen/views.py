from urllib.request import Request

from django.http import HttpResponse
from django.shortcuts import render

from kitchen.models import Dish, DishType, Cook


def index(request: Request) -> HttpResponse:
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()

    context = {
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
    }

    return render(request, "kitchen/index.html", context=context)
