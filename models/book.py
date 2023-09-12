from peewee import CharField, IntegerField, AutoField

from .db import database


class Book(database.Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=100, null=False)
    year_first_published = IntegerField()
