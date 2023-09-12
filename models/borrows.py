from peewee import AutoField, ForeignKeyField, DateField

from .db import database

from .book_copies import BookCopies
from .student import Student


class Borrows(database.Model):
    id = AutoField(primary_key=True)
    book_copy_id = ForeignKeyField(BookCopies, null=False)
    student_id = ForeignKeyField(Student, null=False)
    borrow_date = DateField(null=False)
    return_date = DateField(null=True)
