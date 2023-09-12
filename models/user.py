from peewee import CharField, BooleanField
from hashlib import sha256
from config import AppConfig
from .db import database


class User(database.Model):
    username = CharField(max_length=50)
    email = CharField(max_length=255)
    full_name = CharField()
    password = CharField()
    super = BooleanField(default=False)

    @classmethod
    def from_registration_form(cls, form):
        return cls(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            password=cls.hash_password(form.username.data, form.password.data)
        )

    @staticmethod
    def hash_password(username, password):
        salted_password = f"@@{AppConfig.SALT_KEY}%+%{username}/*-{password}+-*{AppConfig.SALT_KEY}+++"
        hash_generator = sha256(salted_password.encode())
        return hash_generator.hexdigest()
