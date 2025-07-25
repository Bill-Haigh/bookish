import azure.functions as func
import logging
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import os
from datetime import date
from models.models import Base, User
from controllers.books_controller import get_books_handler, post_book_handler

app = func.FunctionApp()

engine = create_engine(os.environ["DB_URL"], echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Helper to calculate age from a date of birth
def _calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@app.route(route="httpget", methods=["GET"])
def http_get(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "World")
    with SessionLocal() as session:
        selection = select(User).where(User.name == name).order_by(User.id.desc())
        user = session.execute(selection).scalar()
        if user and user.date_of_birth:
            age = _calculate_age(user.date_of_birth)
            return func.HttpResponse(f"Hello, {name}! You are {age} years old!")
        return func.HttpResponse(f"Hello, {name}! User record not found.")

@app.route(route="httppost", methods=["POST"])
def http_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        dob_str = req_body.get('dob')

        try:
            dob = date.fromisoformat(dob_str)
        except Exception:
            return func.HttpResponse("'dob' must be in YYYY-MM-DD format", status_code=400)

        with SessionLocal() as session:
            session.add(User(name=name, date_of_birth=dob))
            session.commit()

        logging.info(f"Processing POST request. Name: {name}")

        if name and isinstance(name, str):
            age = _calculate_age(dob)
            return func.HttpResponse(f"Hello, {name}! You are {age} years old!")
        return func.HttpResponse("Please provide both 'name' and 'dob' in the request body.", status_code=400)
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body",
            status_code=400
        )

@app.route(route="books/get", methods=["GET"])
def get_books(req: func.HttpRequest) -> func.HttpResponse:
    return get_books_handler(req, SessionLocal)

@app.route(route="books/post", methods=["POST"])
def post_book(req: func.HttpRequest) -> func.HttpResponse:
    return post_book_handler(req, SessionLocal)
