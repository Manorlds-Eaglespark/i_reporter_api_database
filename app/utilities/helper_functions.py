from app.models.incident import Incident
from flask import make_response, jsonify


class Helper_Functions:

    @staticmethod
    def the_return_method(status, data, message):
        return make_response(jsonify({"status": status, "data": data, "message": message})), status

    @staticmethod
    def get_red_flags():
        red_flags_list = []
        for incident in incidents:
            if incident.type == "red-flag":
                red_flags_list.append(incident.to_json_object())
        return red_flags_list
        
    @staticmethod
    def get_a_red_flag(id):
        for incident in incidents:
            if incident.id == int(id):
                return incident.to_json_object()
    
    @staticmethod
    def get_dict_data_from_list_incident(list_data):
        return {
         			"created_by": list_data[0],
         			"type": list_data[1],
         			"location": list_data[2],
         			"status": list_data[3],
         			"images": list_data[4],
         			"videos": list_data[5],
         			"comment": list_data[6]
        }

    @staticmethod
    def get_dict_data_from_list_user(list_data):
        return {
         			"firstname": list_data[0],
         			"lastname": list_data[1],
         			"othernames": list_data[2],
         			"email": list_data[3],
         			"password": list_data[4],
         			"phonenumber": list_data[5],
         			"username": list_data[6]
        }

    @staticmethod
    def update_location(id, location):
        for incident in incidents:
            if incident.id == int(id):
                incident.location = location
                return incident.to_json_object()

    @staticmethod
    def update_comment(id, comment):
        for incident in incidents:
            if incident.id == int(id):
                incident.comment = comment
                return incident.to_json_object()

    @staticmethod
    def delete_redflag(id):
        for incident in incidents:
            if incident.id == int(id):
                incidents.remove(incident)
                return True
        return False

    @staticmethod
    def email_exists_already(email):
        for user in users:
            if user.email == email:
                return True
        return False
    
    @staticmethod
    def get_user(email):
        for user in users:
            if user.email == email:
                return user

