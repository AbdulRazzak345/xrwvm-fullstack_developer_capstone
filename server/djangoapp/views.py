from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["userName"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            data = {
                "userName": username,
                "status": "Authenticated"
            }

            return JsonResponse(data)

        else:
            data = {
                "userName": username,
                "error": "Invalid credentials"
            }

            return JsonResponse(data)

    return JsonResponse({"error": "POST request required"})


def logout_request(request):
    logout(request)

    data = {
        "userName": ""
    }

    return JsonResponse(data)


@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from request body
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    username_exist = False

    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True

    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:

        # Create user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Login the user
        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }

        return JsonResponse(data)

    else:

        data = {
            "userName": username,
            "error": "Already Registered"
        }

        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.all().count()

    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("make")

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.make.name
        })

    return JsonResponse({
        "CarModels": cars
    })