
import os
from app.views import create_app
from app.database.database import Database

database = Database()
database.create_all_tables()
# database.delete_all_tables()


app = create_app('development')

if __name__ == '__main__':  
    app.run()