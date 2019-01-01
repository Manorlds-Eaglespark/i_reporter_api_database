# # /app/auth/views.py
# from app.utilities.register_validation import Register_Validation
# from app.models.user import User
# from flask import make_response, request, jsonify, abort, json
# from flask.views import MethodView
# from . import auth_blueprint
# import os
# import sys


# class RegistrationView(MethodView):
#     """This class registers a new user."""

#     def post(self):

#         input_data = json.loads(request.data)

#         firstname = input_data['firstname']
#         lastname = input_data['lastname']
#         othernames = input_data['othernames']
#         email = input_data['email']
#         password = input_data['password']
#         phonenumber = input_data['phonenumber']
#         username = input_data['username']

#         validate_input = Register_Validation(
#             {"firstname": firstname, "lastname": lastname, "othernames": othernames, "email": email, "password": password, "phonenumber": phonenumber, "username": username})
#         validated_input = validate_input.check_input()
#         if validated_input[0] == 200:
#             if Helper_Functions.email_exists_already(email) is True:
#                 return make_response(jsonify({"status": 400, "message": "That Email already is registered. Login or use a different Email to register."})), 400
#             else:
#                 new_user_info_list = [
#                     firstname, lastname, othernames, email, password, phonenumber, username]
#                 new_user = User(new_user_info_list)

#                 users.append(new_user)
#                 return make_response(jsonify({"status": 201, "data": new_user.to_json_object(), "message": "You registered successfully. Login to continue."})), 201
#         else:
#             return Helper_Functions.the_return_method(validated_input[0], None, validated_input[1])




# registration_view = RegistrationView.as_view('registration_view')

# auth_blueprint.add_url_rule(
#     '/api/v1/auth/register',
#     view_func=registration_view,
#     methods=['POST'])

