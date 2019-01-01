# app/views.py
import re
from flask import Flask, request, jsonify, make_response, json
from datetime import datetime
from instance.config import app_config
from app.utilities.incident_validation import Incident_Validation


def create_app(config_name):

    from app.models.incident import Incident
    # from app.models.admin import Admin
    from app.models.user import User

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

    @app.route('/api/v1/red-flags', methods=['POST'])
    def create_new_redflag_incident():

        input_data = json.loads(request.data)

        created_by = input_data['created_by']
        doc_type   = input_data['type']
        location   = input_data['location']
        status     = input_data['status']
        images     = input_data['images']
        videos     = input_data['videos']
        comment    = input_data['comment']

        input_list = [created_by, doc_type, location, status, images, videos, comment]

        validate_inputs = Incident_Validation(
            Helper_Functions.get_dict_data_from_list_incident(input_list))

        validated_inputs = validate_inputs.check_types()
        duplicate_exists = Helper_Functions.incident_exists_check(comment)
        
        if validated_inputs[0] == 200:

            if not duplicate_exists:      
                red_flag = Incident(input_list)
                return "Saving incident"
                # incidents.append(red_flag)
                return make_response(jsonify({"status": 201, "data": [{"id":red_flag.id, "message":"Created red-flag record"}]}))
            else:
                return make_response(jsonify({"status": duplicate_exists[0], "error": duplicate_exists[1]}))
                
        else:
            return make_response(jsonify({"status": validated_inputs[0], "error": validated_inputs[1]}))

    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
