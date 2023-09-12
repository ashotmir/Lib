from peewee import AutoField, CharField
from .db import database


class Student(database.Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=50, null=False)
    second_name = CharField(max_length=50, null=False)