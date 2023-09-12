from peewee import CharField, AutoField

from .db import database


class Author(database.Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=50, null=False)
    second_name = CharField(max_length=50, null=False)
