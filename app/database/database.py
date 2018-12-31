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
                                   "registered TIMESTAMP NOT NULL,")")
        self.cursor.execute(sql_command_users_table)
        self.cursor.connection.commit()

    def delete_all_tables(self):
        sql_delete_command_users_table = "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        self.cursor.execute(sql_delete_command_users_table)
