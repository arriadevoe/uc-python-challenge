import datetime
from time import mktime

from flask import Flask, request, make_response, jsonify
import jwt
from jwt.exceptions import DecodeError
import requests

from secrets import api_auth_token, jwt_secret_key
from utils import parse_date_time
from business import get_user_by_email

app = Flask(__name__)


def decode_auth_token(auth_token):
    # use jwt, jwt_secret_key
    # should be a one liner, but we want you to see how JWTs work
    decoded_token = jwt.decode(auth_token, jwt_secret_key, algorithms="HS256")
    return decoded_token


def encode_auth_token(user_id, name, email, scopes):
    # use jwt and jwt_secret_key imported above, and the payload defined below
    # should be a one liner, but we want you to see how JWTs work
    # remember to convert the result of jwt.encode to a string
    # make sure to use .decode("utf-8") rather than str() for this
    payload = {
        "sub": user_id,
        "name": name,
        "email": email,
        "scope": scopes,
        "exp": mktime(
            (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()
        ),
    }

    # didn't end up needing to decode, result already a string
    encoded_token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")
    return encoded_token


def get_user_from_token():
    # use decode_auth_token above and flask.request imported above
    # should pull token from the Authorization header
    # Authorization: Bearer {token}
    # Where {token} is the token created by the login route
    auth_token = request.headers.get("Authorization")
    if auth_token:
        try:
            user_data = decode_auth_token(auth_token)
            return user_data
        except DecodeError:
            response_object = {"Error": "Invalid authorization token"}
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {"Error": "Missing authorization token"}
        return make_response(jsonify(response_object)), 401


@app.route("/")
def status():
    return "API Is Up"


@app.route("/user", methods=["GET"])
def user():
    # get the user data from the auth/header/jwt
    response = get_user_from_token()
    if type(response) == dict:
        return {
            "user_id": response.get("sub"),
            "name": response.get("name"),
            "email": response.get("email"),
        }
    else:
        return response


@app.route("/login", methods=["POST"])
def login():
    # use use flask.request to get the json body and get the email and scopes property
    # use the get_user_by_email function to get the user data
    # return a the encoded json web token as a token property on the json response as in the format below
    # we're not actually validitating a password or anything because that would add unneeded complexity
    request_body = request.get_json()
    login_email = request_body.get("email")
    login_scopes = request_body.get("scopes")

    try:
        users = get_user_by_email(login_email)
        user_id = users.get("id")
        user_name = users.get("name")

        auth_token = encode_auth_token(user_id, user_name, login_email, login_scopes)
        return {"token": auth_token}
    except IndexError:
        response_object = {"Error": "Unable to login"}
        return make_response(jsonify(response_object)), 401


@app.route("/widgets", methods=["GET"])
def widgets():
    # accept the following optional query parameters (using the the flask.request object to get the query params)
    # type, created_start, created_end
    # dates will be in iso format (2019-01-04T16:41:24+0200)
    # dates can be parsed using the parse_date_time function written and imported for you above
    # get the user ID from the auth/header
    # verify that the token has the widgets scope in the list of scopes

    # Using the requests library imported above send the following the following request,

    # GET https://us-central1-interview-d93bf.cloudfunctions.net/widgets?user_id={user_id}
    # HEADERS
    # Authorization: apiKey {api_auth_token}

    # the api will return the data in the following format

    # [ { "id": 1, "type": "floogle", "created": "2019-01-04T16:41:24+0200" } ]
    # dates can again be parsed using the parse_date_time function

    # filter the results by the query parameters
    # return the data in the format below
    get_user_response = get_user_from_token()
    if type(get_user_response) == dict:
        user_id = get_user_response.get("sub")
        scopes = get_user_response.get("scope")
        if "widgets" not in scopes:
            response_object = {"Error": "User does not have widgets scope"}
            return make_response(jsonify(response_object)), 401
    else:
        return get_user_response

    response = requests.get(
        "https://us-central1-interview-d93bf.cloudfunctions.net/widgets",
        headers={"Authorization": f"apiKey {api_auth_token}"},
        params={"user_id": user_id},
    )

    json_response = response.json()
    query_params = dict(request.args)
    query_keys = list(query_params.keys())

    if {"type", "created_start", "created_end"} == set(query_keys):
        filtered_response = [
            widget
            for widget in json_response
            if widget["type"] == query_params["type"]
            and parse_date_time(widget["created"])
            >= parse_date_time(query_params["created_start"])
            and parse_date_time(widget["created"])
            <= parse_date_time(query_params["created_end"])
        ]
    elif {"type", "created_start"} == set(query_keys):
        filtered_response = [
            widget
            for widget in json_response
            if widget["type"] == query_params["type"]
            and parse_date_time(widget["created"])
            >= parse_date_time(query_params["created_start"])
        ]
    elif {"type", "created_end"} == set(query_keys):
        filtered_response = [
            widget
            for widget in json_response
            if widget["type"] == query_params["type"]
            and parse_date_time(widget["created"])
            <= parse_date_time(query_params["created_end"])
        ]
    elif {"created_start", "created_end"} == set(query_keys):
        filtered_response = [
            widget
            for widget in json_response
            if parse_date_time(widget["created"])
            >= parse_date_time(query_params["created_start"])
            and parse_date_time(widget["created"])
            <= parse_date_time(query_params["created_end"])
        ]
    elif ["type"] == query_keys:
        filtered_response = [
            widget for widget in json_response if widget["type"] == query_params["type"]
        ]
    elif ["created_start"] == query_keys:
        filtered_response = [
            widget
            for widget in json_response
            if parse_date_time(widget["created"])
            >= parse_date_time(query_params["created_start"])
        ]
    elif ["created_end"] == query_keys:
        filtered_response = [
            widget
            for widget in json_response
            if parse_date_time(widget["created"])
            <= parse_date_time(query_params["created_end"])
        ]
    else:
        filtered_response = json_response

    for widget in filtered_response:
        widget["type_label"] = widget["type"].replace("-", " ").title()

    return {
        "total_widgets_owned_by_user": len(filtered_response),
        "matching_items": filtered_response,
    }


if __name__ == "__main__":
    app.run()
