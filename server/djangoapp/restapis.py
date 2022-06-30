import requests
import json
from .models import CarDealer, DealerReview # import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            # Basic authentication GET
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print(params)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object

            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                    full_name=dealer["full_name"], id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

#get dealer by Id
def get_dealer_by_id(url, id):
    json_result = get_request(url, id=id)
    results = []
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object

            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                    full_name=dealer["full_name"], id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
#def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
   

    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]["rows"]["docs"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object

            #dealer_doc = dealer["doc"]
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], id=review["id"], dealership=review["dealership"], name=review["name"],
                                   purchase=review["purchase"], purchase_date=review["purchase_date"], review=review["review"])
            
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment

            results.append(review_obj)

        
    

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/27b38454-f3f7-42db-aa15-ca6d843ac564"
    api_key = "lBjvPn8_JYSRUStwnDKtd04UoadgOE18Fsnhzbil5llx"
    response = get_request(url, text=text, api_key=api_key, version='2020-08-01', features='sentiment', return_analyzed_text=True)
    print(response)
    return response


