import os
import requests
import jwt

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

from flask import make_response, request, jsonify
from dao import users


def handle_oauth_slack():
    data = request.json
    print(data)

    code = data["code"]

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    redirect_uri = os.getenv('SLACK_REDIRECT_URL')
    client_id = os.getenv('SLACK_CLIENT_ID')
    client_secret = os.getenv('SLACK_CLIENT_SECRET')

    payload = 'code=' + code + '&redirect_uri=' + redirect_uri + \
        '&client_id=' + client_id + '&client_secret=' + client_secret

    url = "https://slack.com/api/openid.connect.token"

    response = requests.post(url, headers=headers, data=payload)
    print("Slack API:", response.status_code, response.json())

    res_json = response.json()

    # Parse & Verfiy JWT (https://slack.com/openid/connect/keys)
    jwt_data = decode_jwt(data=res_json, client_id=client_id)

    slack_user_id = jwt_data["https://slack.com/user_id"]
    slack_team_id = jwt_data["https://slack.com/team_id"]
    access_token = res_json["access_token"]
    email = jwt_data["email"]
    name = jwt_data["name"]
    img_url = jwt_data["picture"]

    # TODO: Check if the user already has an account
    existing_user = users.find_by_slack_id(slack_user_id=slack_user_id)
    if existing_user is not None:
        res = make_response(jsonify({"sucesss": True}))
        res.set_cookie("user_id", slack_user_id,
                       httponly="true", samesite="none", secure="true")
        # res.headers["Access-Control-Allow-Credentials"] = "true"
        return res, 200

    users.create(slack_user_id=slack_user_id, slack_team_id=slack_team_id,
                 email=email, name=name, profile_img=img_url, access_token=access_token)

    res = make_response(jsonify({"sucesss": True}))
    res.set_cookie("user_id", slack_user_id, httponly="true",
                   samesite="none", secure="true")
    # res.headers["Access-Control-Allow-Credentials"] = "true"
    return res, 200


def decode_jwt(data, client_id):
    print(data)

    req = requests.get('https://slack.com/openid/connect/keys')
    jwks = req.json()
    print(jwks)

    # Extracting the first key (assuming only one key is present)
    key = jwks['keys'][0]

    # Base64 URL decode the exponent and modulus
    e = int.from_bytes(base64.urlsafe_b64decode(key['e'] + '=='), 'big')
    n = int.from_bytes(base64.urlsafe_b64decode(key['n'] + '=='), 'big')

    # Create the RSA public key
    public_key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())

    # Serialize the public key to PEM format
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Print the PEM formatted public key
    print(pem.decode('utf-8'))

    # Decode the JWT
    try:
        decoded_jwt = jwt.decode(
            data["id_token"], pem, algorithms=["RS256"], audience=client_id)
        print(decoded_jwt)
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
