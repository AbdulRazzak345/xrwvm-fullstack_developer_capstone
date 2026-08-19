from .restapis import get_request, analyze_review_sentiments, post_review
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)


# ============================================================
# LOGIN
# ============================================================

@csrf_exempt
def login_user(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            username = data["userName"]
            password = data["password"]

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                return JsonResponse({
                    "userName": username,
                    "status": "Authenticated"
                })

            return JsonResponse({
                "userName": username,
                "error": "Invalid credentials"
            })

        except Exception as e:
            logger.exception("Login error")

            return JsonResponse({
                "error": str(e)
            }, status=400)

    return JsonResponse({
        "error": "POST request required"
    }, status=400)


# ============================================================
# LOGOUT
# ============================================================

def logout_request(request):

    logout(request)

    return JsonResponse({
        "userName": ""
    })


# ============================================================
# REGISTRATION
# ============================================================

@csrf_exempt
def registration(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"
        }, status=400)

    try:
        data = json.loads(request.body)

        username = data["userName"]
        password = data["password"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]

        # Check if username already exists
        if User.objects.filter(username=username).exists():

            return JsonResponse({
                "userName": username,
                "error": "Already Registered"
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Login immediately
        login(request, user)

        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        })

    except Exception as e:

        logger.exception("Registration error")

        return JsonResponse({
            "error": str(e)
        }, status=400)


# ============================================================
# GET CAR MAKES AND MODELS
# ============================================================

def get_cars(request):

    count = CarMake.objects.all().count()

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


# ============================================================
# GET ALL DEALERSHIPS / DEALERS BY STATE
# ============================================================

def get_dealerships(request, state="All"):

    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


# ============================================================
# GET SINGLE DEALER
# ============================================================

def get_dealer_details(request, dealer_id):

    if dealer_id:

        endpoint = "/fetchDealer/" + str(dealer_id)

        dealer = get_request(endpoint)

        return JsonResponse({
            "status": 200,
            "dealer": dealer
        })

    return JsonResponse({
        "status": 400,
        "message": "Bad Request"
    }, status=400)


# ============================================================
# GET DEALER REVIEWS
# ============================================================

def get_dealer_reviews(request, dealer_id):

    if not dealer_id:

        return JsonResponse({
            "status": 400,
            "message": "Bad Request"
        }, status=400)

    endpoint = "/fetchReviews/dealer/" + str(dealer_id)

    reviews = get_request(endpoint)

    # Make sure reviews is a list
    if reviews is None:
        reviews = []

    # Analyze sentiment for each review
    for review_detail in reviews:

        try:

            response = analyze_review_sentiments(
                review_detail.get("review", "")
            )

            print("Sentiment response:", response)

            # IMPORTANT:
            # The sentiment service may be unavailable.
            # Do not crash the entire endpoint.

            if response and isinstance(response, dict):

                review_detail["sentiment"] = response.get(
                    "sentiment",
                    "unknown"
                )

            else:

                review_detail["sentiment"] = "unknown"

        except Exception as e:

            logger.exception(
                "Sentiment analysis failed"
            )

            review_detail["sentiment"] = "unknown"

    return JsonResponse({
        "status": 200,
        "reviews": reviews
    })


# ============================================================
# ADD REVIEW
# ============================================================

@csrf_exempt
def add_review(request):

    print("========== ADD REVIEW ==========")
    print("User:", request.user)
    print(
        "Authenticated:",
        request.user.is_authenticated
    )

    if request.method != "POST":

        return JsonResponse({
            "status": 400,
            "message": "POST request required"
        }, status=400)

    # User must be logged in
    if request.user.is_anonymous:

        return JsonResponse({
            "status": 403,
            "message": "Unauthorized"
        }, status=403)

    try:

        data = json.loads(request.body)

        print("Review data:")
        print(data)

        response = post_review(data)

        print("post_review response:")
        print(response)

        if response:

            return JsonResponse({
                "status": 200,
                "message": "Review posted successfully"
            })

        return JsonResponse({
            "status": 500,
            "message": "Unable to post review"
        }, status=500)

    except Exception as e:

        logger.exception(
            "Error in posting review"
        )

        return JsonResponse({
            "status": 500,
            "message": "Error in posting review",
            "error": str(e)
        }, status=500)