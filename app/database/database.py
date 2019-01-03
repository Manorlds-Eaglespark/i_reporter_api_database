import psycopg2
import os


class Database:

    """docstring for Database class"""

    def __init__(self):
        # db_name = os.getenv("DATABASE")
        db_name = "ireporter"
        self.connection = psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432",
                                           database=db_name)
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def create_all_tables(self):
        sql_command_users_table = ("CREATE TABLE IF NOT EXISTS users"
                                   "(id SERIAL PRIMARY KEY,"
                                   "firstname TEXT NOT NULL,"
                                   "lastname TEXT NOT NULL,"
                                   "othernames TEXT NULL,"
                                   "email TEXT NOT NULL,"
                                   "password TEXT NOT NULL,"
                                   "phonenumber TEXT NOT NULL,"
                                   "username TEXT NOT NULL,"
                                   "isadmin TEXT NOT NULL,"
                                   "registered TIMESTAMP NOT NULL)")
        sql_command_incidents_table = ("CREATE TABLE IF NOT EXISTS incidents"
                                   "(id SERIAL PRIMARY KEY,"
                                   "created_on TIMESTAMP NOT NULL,"
                                   "created_by INTEGER NOT NULL,"
                                   "type TEXT NULL,"
                                   "location TEXT NOT NULL,"
                                   "status TEXT NOT NULL,"
                                   "images TEXT NOT NULL,"
                                   "videos TEXT NOT NULL,"
                                   "comment TEXT NOT NULL)")
        self.cursor.execute(sql_command_users_table)
        self.cursor.execute(sql_command_incidents_table)
        self.cursor.connection.commit()


    def get_registered_user(self, email):
        sql_select_user_query = """SELECT * FROM users WHERE email = '{0}'""".format(email)
        self.cursor.execute(sql_select_user_query)
        user = self.cursor.fetchone()
        return user

    def save_user(self, user):
        postgres_insert_user_query = ("INSERT INTO users ("
                                        "firstname, lastname, othernames, email, password, phonenumber,"
                                        "username, registered, isadmin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        record_to_insert = (user.firstname, user.lastname, user.othernames, user.email, user.password, user.phonenumber, user.username, user.registered, user.isadmin)
        self.cursor.execute(postgres_insert_user_query, record_to_insert)
        saved_user = self.get_registered_user(user.email)
        return saved_user[0]   #return user id.

    def get_like_this_in_database(self, comment, created_by):
        postgresql_select_incidents_query = """SELECT * FROM incidents where comment = %s and created_by = %s"""
        self.cursor.execute(
            postgresql_select_incidents_query, (comment, created_by))
        incident = self.cursor.fetchone()
        return incident

    def save_incident(self, incident):
        postgres_insert_incident_query = ("INSERT INTO incidents ("
                                        "created_on, created_by, type, location, status,"
                                        "images, videos, comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
        record_to_insert = (incident.created_on, incident.created_by,
                            incident.type, incident.location, incident.status, incident.images, incident.videos, incident.comment)
        self.cursor.execute(postgres_insert_incident_query, record_to_insert)
        saved_incident = self.get_like_this_in_database(incident.comment, incident.created_by)
        return saved_incident[0]    #return only id from returned incident tuple

    def get_all_red_flags(self):
        sql_get_red_flags_query = """SELECT * FROM incidents where type='red-flag'"""
        self.cursor.execute(sql_get_red_flags_query)
        red_flags = self.cursor.fetchall()
        return red_flags

    def get_incident_by_id(self, id):
        sql_select_incident_query = """SELECT * FROM incidents WHERE id = {0}""".format(id)
        self.cursor.execute(sql_select_incident_query)
        incident = self.cursor.fetchone()
        return incident

    def update_location_of_incident(self, incident_id, new_location):
        sql_update_incident_location = """UPDATE incidents SET location = %s WHERE id = %s"""
        self.cursor.execute(sql_update_incident_location,(new_location, incident_id))
        
    def update_comment_of_incident(self, incident_id, new_comment):
        sql_update_incident_comment = """UPDATE incidents SET comment = %s WHERE id = %s"""
        self.cursor.execute(sql_update_incident_comment,(new_comment, incident_id))

    def delete_incident(self, incident_id):
        sql_delete_incident = "DELETE FROM incidents WHERE id = {0}".format(incident_id)
        self.cursor.execute(sql_delete_incident)

    def delete_all_tables(self):
        sql_delete_command_users_table = "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        sql_delete_command_incidents_table="TRUNCATE TABLE incidents RESTART IDENTITY CASCADE"
        self.cursor.execute(sql_delete_command_users_table)
        self.cursor.execute(sql_delete_command_incidents_table)
