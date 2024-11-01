# app/routes.py
from fastapi import APIRouter, HTTPException
from app.models import UserCreate, User
from app.models import FineCreate, Fine
from app.models import Publisher, PublisherCreate
from app.models import Event, EventCreate
from app.models import BookCreate, Book
from app.models import Loan, LoanCreate
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

@router.post("/publishers/", response_model=List[Publisher])
def create_publishers_bulk(publishers: List[PublisherCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_publishers = []
        for publisher in publishers:
            query = """
            INSERT INTO publishers (publisher_name, country, foundation_year)
            VALUES (%s, %s, %s)
            """
            values = (publisher.publisher_name, publisher.country, publisher.foundation_year)
            
            cursor.execute(query, values)
            publisher_id = cursor.lastrowid
            created_publishers.append(Publisher(id=publisher_id, **publisher.dict()))
        
        conn.commit()
        return created_publishers
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/publishers/", response_model=List[Publisher])
def list_publishers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM publishers"
        cursor.execute(query)
        publishers = cursor.fetchall()
        return [Publisher(**publisher) for publisher in publishers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/events/", response_model=List[Event])
def create_events_bulk(events: List[EventCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_events = []
        for event in events:
            query = """
            INSERT INTO events (event_name, description, event_date, event_type, capacity)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (event.event_name, event.description, event.event_date, event.event_type, event.capacity)
            
            cursor.execute(query, values)
            event_id = cursor.lastrowid
            created_events.append(Event(id=event_id, **event.dict()))
        
        conn.commit()
        return created_events
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/events/", response_model=List[Event])
def list_events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM events"
        cursor.execute(query)
        events = cursor.fetchall()
        return [Event(**event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/books/", response_model=List[Book])
def create_books_bulk(books: List[BookCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_books = []
        for book in books:
            # Verifica si el publisher_id existe en la tabla `publishers`
            cursor.execute("SELECT id FROM publishers WHERE id = %s", (book.publisher_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Publisher with id {book.publisher_id} not found")

            # Inserta el libro
            query = """
            INSERT INTO books (title, author, category, publication_year, status, type, publisher_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (book.title, book.author, book.category, book.publication_year, book.status, book.type, book.publisher_id)
            cursor.execute(query, values)
            book_id = cursor.lastrowid
            created_books.append(Book(id=book_id, **book.dict()))

        conn.commit()
        return created_books
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/books/", response_model=List[Book])
def list_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Recupera todos los registros de la tabla `books`
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return [Book(**book) for book in books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/loans/", response_model=List[Loan])
def create_loans_bulk(loans: List[LoanCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        created_loans = []
        for loan in loans:
            # Verifica si el user_id existe en la tabla `users`
            cursor.execute("SELECT id FROM users WHERE id = %s", (loan.user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"User with id {loan.user_id} not found")

            # Verifica si el book_id existe en la tabla `books`
            cursor.execute("SELECT id FROM books WHERE id = %s", (loan.book_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Book with id {loan.book_id} not found")

            # Inserta el préstamo
            query = """
            INSERT INTO loans (book_id, user_id, loan_date, return_date, renewals, status, librarian_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (loan.book_id, loan.user_id, loan.loan_date, loan.return_date, loan.renewals, loan.status, loan.librarian_id)
            cursor.execute(query, values)
            loan_id = cursor.lastrowid
            created_loans.append(Loan(id=loan_id, **loan.dict()))

        conn.commit()
        return created_loans
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/loans/", response_model=List[Loan])
def get_loans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM loans")
        loans = cursor.fetchall()
        return [Loan(**loan) for loan in loans]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()