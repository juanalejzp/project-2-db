import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME")
    )