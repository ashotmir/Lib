from peewee import ForeignKeyField
from .book import Book
from .author import Author
from .db import database


class BookAuthor(database.Model):
    book_id = ForeignKeyField(Book)
    author_id = ForeignKeyField(Author)

    class Meta:
        primary_key = False
