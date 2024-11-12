from project import db, app

from datetime import datetime
import re


# Book model
class Book(db.Model):
    NAME_PATTERN = r"^[A-Za-z0-9\s\-_,\.;:()']+$"
    AUTHOR_PATTERN = r"^[A-Za-z]+([' -][A-Za-z]+)*$"

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer) 
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = Book.validate_name(name)
        self.author = Book.validate_author(author)
        self.year_published = Book.validate_year_published(int(year_published))
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

    @staticmethod
    def validate_name(name: str): 
        if not isinstance(name, str):
            raise ValueError("Parameter name - must be a valid string")
        if len(name) <= 2 or len(name) > 64:
            raise ValueError("Parameter name - length must be between 3 to 64 characters")
        if not re.match(Book.NAME_PATTERN, name):
            raise ValueError("Parameter name - must contain only allowed characters A-Za-z0-9-_,.;:()'")
        return name



    @staticmethod
    def validate_author(author: str):
        if not isinstance(author, str):
            raise ValueError("Parameter author - must be a valid string")
        if len(author) <= 1 or len(author) > 64:
            raise ValueError("Parameter author - length must be between 2 to 64 characters")
        if not re.match(Book.AUTHOR_PATTERN, author):
            raise ValueError("Parameter author - must contain only allowed characters A-Za-z0-9-'")
        return author

    @staticmethod
    def validate_year_published(year_published: int):
        current_year = datetime.now().year

        if not isinstance(year_published, int):
            raise ValueError("Parameter year_published - must be a valid number")
        if year_published < 1000:
            raise ValueError("Parameter year_published - smallest possible year: 1000 ")
        if year_published > current_year:
            raise ValueError("Parameter year_published - publication year cannot be set into future")    
        return year_published


with app.app_context():
    db.create_all()