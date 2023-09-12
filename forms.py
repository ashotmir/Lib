from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import InputRequired, EqualTo, NumberRange, Length

from datetime import datetime
dt = datetime.now().year


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
        ],
    )
    password = StringField(
        validators=[
            InputRequired(),
        ],
    )


class RegisterStudentForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
        ]
    )
    password = StringField(
        validators=[
            InputRequired(),
        ]
    )
    repeat_password = StringField(
        validators=[
            EqualTo("password",
                    message="Passwords don't match")
        ]
    )
    full_name = StringField(
        validators=[
            InputRequired()
        ]
    )
    email = EmailField(
        validators=[
            InputRequired(),
        ]
    )


class RegisterEmployeeForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
        ]
    )
    password = StringField(
        validators=[
            InputRequired(),
        ]
    )
    repeat_password = StringField(
        validators=[
            EqualTo("password",
                    message="Passwords don't match")
        ]
    )
    full_name = StringField(
        validators=[
            InputRequired()
        ]
    )
    email = EmailField(
        validators=[
            InputRequired(),
        ]
    )
    special_code = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1000, max=dt)
        ]
    )


class BookAddForm(FlaskForm):
    title = StringField(
        validators=[
            InputRequired(),
        ],
    )
    year_first_published = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1000, max=2023)
        ],
    )
    first_name = StringField(
        validators=[
            InputRequired(),
        ]
    )
    second_name = StringField(
        validators=[
            InputRequired(),
        ]
    )
    quantity = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1)

        ]
    )
    isbn = StringField(
        validators=[
            InputRequired(),
            Length(min=10, max=13)
        ]
    )
    year_published = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=1000, max=dt)
        ]
    )


class BorrowTakeForm(FlaskForm):
    book_title = StringField(
        validators=[
            InputRequired(),
        ],
    )

    student_id = IntegerField(
        validators=[
            InputRequired(),
        ],
    )
