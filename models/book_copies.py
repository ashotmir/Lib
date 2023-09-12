from peewee import AutoField, ForeignKeyField, IntegerField, BigIntegerField, BooleanField
from .db import database
from .book import Book


class BookCopies(database.Model):
    id = AutoField(primary_key=True)
    book_id = ForeignKeyField(Book, null=False)
    ISBN = BigIntegerField()
    year_published = IntegerField(null=False)
    available = BooleanField(default=True)