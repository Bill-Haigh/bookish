from sqlalchemy import select
from models.models import Book
import azure.functions as func
import json

def get_books_handler(req, SessionLocal):
    with SessionLocal() as session:
        books = session.execute(select(Book)).scalars().all()
        books_list = [
            {
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "total_copies": book.total_copies
            }
            for book in books
        ]
        return func.HttpResponse(json.dumps(books_list), mimetype="application/json")

def post_book_handler(req, SessionLocal):
    try:
        req_body = req.get_json()
        isbn = req_body.get('isbn')
        title = req_body.get('title')
        author = req_body.get('author')
        total_copies = req_body.get('total_copies')

        if not all([isbn, title, author, total_copies]):
            return func.HttpResponse("Missing required book fields.", status_code=400)

        with SessionLocal() as session:
            session.add(Book(isbn=isbn, title=title, author=author, total_copies=total_copies))
            session.commit()

        return func.HttpResponse(f"Book '{title}' added successfully!", status_code=201)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=400)