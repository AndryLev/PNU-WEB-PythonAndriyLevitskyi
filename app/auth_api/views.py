import datetime

import jwt
from flask import jsonify, request, current_app
from functools import wraps
from app.auth.models import User
from . import auth_api_blueprint

def get_token(username):
    payload = {
        'exp': datetime.datetime.utcnow() +
        datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sab': username
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token is expired."
    except jwt.InvalidTokenError:
        return "Invalid token."

def required_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        jwt_error = None

        if not token:
            return jsonify({
                "errorMessage": "Token is missing",
            }), 401
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            jwt_error = "Token is expired."
        except jwt.InvalidTokenError:
            jwt_error = "Invalid token"
        if jwt_error:
            return jsonify({"errorMessage": str(jwt_error)}), 401

        return f(*args, **kwargs)

    return decorated

def required_token_second(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        jwt_error = None

        if not token:
            return {
                "errorMessage": "Token is missing",
            }, 401
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            jwt_error = "Token is expired."
        except jwt.InvalidTokenError:
            jwt_error = "Invalid token"
        if jwt_error:
            return {"errorMessage": str(jwt_error)}, 401

        return f(*args, **kwargs)

    return decorated
@auth_api_blueprint.route('/ping' , methods= ["GET", "POST"])
@required_token
def ping():
    return "pong"


@auth_api_blueprint.route("/login", methods=['POST'])
def login():
    post_data = request.get_json()

    if not post_data:
        return jsonify(errorMessage="JSOM payload must be provided"),400

    email = post_data.get("email")
    password = post_data.get("password")

    if not email or not password:
        return jsonify(errorMessage="Email and password are required")

    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
        token = get_token(email)
        return jsonify({"token": token}), 200
    else:
        return jsonify(errorMessage="Incorrect email or password"), 401