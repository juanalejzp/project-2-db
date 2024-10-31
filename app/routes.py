# app/routes.py
from fastapi import APIRouter, HTTPException
from app.models import UserCreate, User
from app.database import get_db_connection
from typing import List

router = APIRouter()

@router.post("/users/", response_model=List[User])
def create_users_bulk(users: List[UserCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_users = []
        for user in users:
            query = """
            INSERT INTO users (name, address, phone, email, registration_date, user_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (user.name, user.address, user.phone, user.email, user.registration_date, user.user_type)

            cursor.execute(query, values)
            user_id = cursor.lastrowid
            created_users.append(User(id=user_id, **user.dict()))

        conn.commit()
        return created_users
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/users/", response_model=List[User])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return [User(**user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
