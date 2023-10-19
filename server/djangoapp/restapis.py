import requests
import json
import os.path
import numpy
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

BASE = os.path.dirname(os.path.abspath(__file__))

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = 0

    if api_key:
       params = dict()
       params["text"] = kwargs["text"]
       params["version"] = kwargs["version"]
       params["features"] = kwargs["features"]
       params["return_analyzed_text"] = kwargs["return_analyzed_text"]
       response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
       return response
    else:
        if url == "dealer-get":
            with open(os.path.join(BASE,'data/dealerships.json')) as file:
                json_data = json.load(file)
        if url == "review-get":
            with open(os.path.join(BASE,'data/reviews.json')) as file:
                json_data = json.load(file)
        return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    # requests.post(url, params=kwargs, json=json_payload)
    return 'True'

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(dealerId):
    url = "dealer-get"
    results = {}
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] == dealerId:
                results = dealer_doc
    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            review_obj = review
            review_obj["sentiment"] = analyze_review_sentiments(review_obj["review"])
            review_obj["dealership_full_name"] = get_dealer_by_id(dealerId)
            if review_obj["dealership"] == dealerId:                
                review_obj = DealerReview( review=review_obj["review"], car_make=review_obj["car_make"],
                                   car_model=review_obj["car_model"],car_year=review_obj["car_year"],
                                   sentiment=review_obj["sentiment"], id=review_obj["id"], dealership_full_name = review_obj["dealership_full_name"])
                results.append(review_obj)

    print(results)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    return 'positive'

def get_dealer_by_id(dealerId):
    result = get_dealer_by_id_from_cf(dealerId)
    return result["full_name"]


