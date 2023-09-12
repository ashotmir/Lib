import math
import random

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from forms import (
    LoginForm,
    RegisterStudentForm,
    RegisterEmployeeForm,
    BookAddForm,
    BorrowTakeForm,
)

from models import (
    Book,
    User,
    BookAuthor,
    Author,
    Student,
    Borrows,
    BookCopies
)

from login import login_required, login_super
from check_book import AddBook

from borrow_func import (
    available_check,
    borrow_book,
    book_return,
    student_books,
    author_books,
)

app = Flask(
    __name__,
    static_url_path="/media",
)

app.config.from_object("config.AppConfig")
pass_code = 0


@app.context_processor
def inject_data() -> dict:
    user_id = session.get("user")
    user_super = None
    user = None
    if user_id:
        user = User.get(user_id)
        user_super = user.super

    return {
        "user": user,
        "super": user_super
    }


@app.route("/")
def home():
    photo_url = url_for("static", filename="home.jpeg")
    return render_template("home.html", photo_url=photo_url)


@app.route("/book")
@login_required
def book():
    photo_url = url_for("static", filename="home.jpeg")
    page_size = 10
    total_pages = math.ceil(Book.select().count() / page_size)
    page_number = int(request.args.get("page", 1))
    books = Book.select().order_by(Book.id).paginate(page_number, page_size)
    return render_template("book/book.html", books=books, total_pages=total_pages,photo_url=photo_url)


@app.route("/book/<int:book_id>")  # Dynamic routing
@login_required
def book_details(book_id):
    available = available_check(book_id)
    title = Book.get(id=book_id)
    author_id = BookAuthor.get(book_id=book_id).author_id
    author = Author.get(id=author_id)
    return render_template("book/book_detalis.html", book=title, author=author, available=available)


@app.route("/book/new", methods=["GET", "POST"])
@login_super
def book_add():
    form = BookAddForm()
    if form.validate_on_submit():
        AddBook.create_book(form)
        return redirect("/")
    return render_template("book/book_add.html", form=form)


@app.route("/author")
@login_required
def author():
    page_size = 10
    total_pages = math.ceil(Author.select().count() / page_size)
    page_number = int(request.args.get("page", 1))
    authors = Author.select().order_by(Author.id).paginate(page_number, page_size)
    return render_template("author/author.html", authors=authors, total_pages=total_pages)


@app.route("/author/<int:author_id>")
@login_required
def author_detalis(author_id):
    author_name = Author.get(id=author_id)
    books = author_books(author_id)
    return render_template("author/author_detalis.html", author=author_name, books=books)


@app.route("/student")
@login_super
def student():
    page_size = 10
    total_pages = math.ceil(Student.select().count() / page_size)
    page_number = int(request.args.get("page", 1))
    students = Student.select().order_by(Student.id).paginate(page_number, page_size)
    return render_template("student/student.html", students=students, total_pages=total_pages)


@app.route("/student/<int:student_id>")
@login_super
def student_details(student_id):
    student = Student.get(id=student_id)
    books = student_books(student_id)
    return render_template("student/student_detalis.html", student=student, books=books)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.get(username=form.username.data)
            hashed_password = User.hash_password(form.username.data, form.password.data)
        except User.DoesNotExist:
            form.username.errors.append("Invalid credentials")
            return render_template("login.html", form=form)
        if user.password != hashed_password:
            form.username.errors.append("Invalid credentials")
            return render_template("login.html", form=form)
        session["user"] = user.id
        session["super"] = user.super
        return_url = request.args.get("next")
        return redirect(return_url if return_url else "/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session["user"] = None
    session["super"] = None
    return redirect("/login")


@app.route("/register/student",  methods=["GET", "POST"])
def register_student():
    form = RegisterStudentForm()
    if form.validate_on_submit():
        user = User().from_registration_form(form)
        user.save()
        return redirect("/")
    return render_template("register/register_student.html", form=form)


@app.route("/register/employee", methods=["GET", "POST"])
def register_employee():
    global pass_code
    if request.method == "GET":
        pass_code = random.randint(999, 10000)
        print(pass_code)
    form = RegisterEmployeeForm()
    if form.special_code.data == pass_code:
        if form.validate_on_submit():
            user = User().from_registration_form(form)
            user.super = True
            user.save()
            return redirect("/")
    return render_template("register/register_employee.html", form=form)


@app.route("/borrow/take",  methods=["GET", "POST"])
@login_super
def take_book():
    form = BorrowTakeForm()
    if form.validate_on_submit():
        if borrow_book(form.book_title.data, form.student_id.data):
            return redirect(f"/student/{form.student_id.data}")
        else:
            return render_template("borrow/borrow_error.html"), 404
    return render_template("borrow/borrow_take.html", form=form)


@app.route("/borrow/return", methods=["GET", "POST"])
@login_super
def return_book():
    form = BorrowTakeForm()
    if form.validate_on_submit():
        if book_return(form.book_title.data, form.student_id.data):
            return redirect("/book")
        else:
            return render_template("borrow/borrow_error.html"), 404
    return render_template("borrow/borrow_return.html", form=form)


@app.route("/borrow/all")
@login_super
def all_borrow():
    page_size = 10
    total_pages = math.ceil(Borrows.select().count() / page_size)
    page_number = int(request.args.get("page", 1))
    borrows = Borrows.select().order_by(Borrows.id).paginate(page_number, page_size)
    # books = BookCopies.get(BookCopies.id.in_(borrows))
    return render_template("borrow/borrow_all.html", total_pages=total_pages, borrows=borrows)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
