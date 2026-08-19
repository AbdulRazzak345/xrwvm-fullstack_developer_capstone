import requests
import logging

logger = logging.getLogger(__name__)


# ============================================================
# BASE URLS
# ============================================================

NODE_SERVER = "http://localhost:3030"
SENTIMENT_SERVER = "http://localhost:5050"


# ============================================================
# GENERIC GET REQUEST
# ============================================================

def get_request(endpoint):

    url = NODE_SERVER + endpoint

    print("GET from", url, "?")

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        print("Network exception occurred:", e)

        return None

    except Exception as e:

        print("Exception occurred:", e)

        return None


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def analyze_review_sentiments(review):

    url = SENTIMENT_SERVER + "/analyze/" + review

    print(
        "GET from",
        url,
        "?"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(
            "Sentiment analyzer response:",
            result
        )

        return result

    except requests.exceptions.RequestException as e:

        print(
            "Network exception occurred:",
            e
        )

        return None

    except Exception as e:

        print(
            "Sentiment analysis exception:",
            e
        )

        return None


# ============================================================
# POST REVIEW
# ============================================================

def post_review(data):

    url = NODE_SERVER + "/insert_review"

    print("POST to", url)

    print(data)

    try:

        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(
            "post_review response:"
        )

        print(result)

        return result

    except requests.exceptions.RequestException as e:

        print(
            "Network exception occurred:",
            e
        )

        return None

    except Exception as e:

        print(
            "Post review exception:",
            e
        )

        return None