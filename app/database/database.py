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

    def delete_all_tables(self):
        sql_delete_command_users_table = "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        sql_delete_command_incidents_table="TRUNCATE TABLE incidents RESTART IDENTITY CASCADE"
        self.cursor.execute(sql_delete_command_users_table)
        self.cursor.execute(sql_delete_command_incidents_table)
