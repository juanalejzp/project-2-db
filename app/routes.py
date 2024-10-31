# app/routes.py
from fastapi import APIRouter, HTTPException
from app.models import UserCreate, User
from app.models import FineCreate, Fine
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

@router.post("/users/{user_id}/fines/", response_model=List[Fine])
def create_fines_bulk(user_id: int, fines: List[FineCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        created_fines = []
        for fine in fines:
            query = """
            INSERT INTO fines (user_id, reason, start_date, end_date, amount)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (user_id, fine.reason, fine.start_date, fine.end_date, fine.amount)
            
            cursor.execute(query, values)
            fine_id = cursor.lastrowid
            # Elimina user_id del diccionario de valores ya que se pasa directamente en la función
            fine_data = fine.dict(exclude={"user_id"})
            created_fines.append(Fine(id=fine_id, user_id=user_id, **fine_data))
        
        conn.commit()
        return created_fines
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/fines/", response_model=List[Fine])
def get_all_fines():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener todas las multas
        cursor.execute("SELECT * FROM fines")
        fines = cursor.fetchall()
        
        return [Fine(**fine) for fine in fines]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()