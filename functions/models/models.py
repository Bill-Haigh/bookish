from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    loans = relationship("Loan", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    isbn = Column(String(20), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    total_copies = Column(Integer, nullable=False)
    loans = relationship("Loan", back_populates="book")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_isbn = Column(String(20), ForeignKey("books.isbn"), nullable=False)
    due_date = Column(Date, nullable=False)
    copies_borrowed = Column(Integer, nullable=False)
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")