# /app/auth/views.py
from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort, json
from app.models.user import User
from app.database.database import Database
import re

database = Database()


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/register"""
        data = json.loads(request.data)
        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        email = data['email']
        password = data['password']
        phonenumber = data['phonenumber']
        username = data['username']

        user = database.get_registered_user(email)

        if not user:
            try:
                user_detail = [firstname, lastname, othernames, email, password, phonenumber, username]
                user = User(user_detail)
                id = database.save_user(user)
                return make_response(jsonify({"status": 201, "data": [{"id": id, "message": "You registered successfully. Please log in."}]})), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
                'error': 'User already exists. Please login.', 
                'status':403
            }
            return make_response(jsonify(response)), 403





class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/login"""
        
        password = json.loads(request.data)['password']
        email = json.loads(request.data)['email']

        if password == "":
            return make_response(jsonify({"message":"Please enter a valid Password."})), 401

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return make_response(jsonify({"message":"Please enter a valid Email."})), 401

        try:
            user_data = database.get_registered_user(email)
            if user_data:
                if user_data and User.password_is_valid(user_data[5], password):
                    access_token = User.generate_token(user_data[0], user_data[8])
                    if access_token:
                        return make_response(jsonify({"status": 200, "data": [{"message": "You logged in successfully.", 'access_token':  access_token.decode()}]})), 200
                else:
                    response = {
                        'message': 'Invalid Password, Please try again'
                    }
                    return make_response(jsonify(response)), 403
            else:
                response = {
                    'message': 'No account by that Email, please register first.'
                }
                return make_response(jsonify(response)), 400

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']

)