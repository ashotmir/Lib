from models import BookCopies, Borrows, Book, BookAuthor
from datetime import date

today = date.today()


def available_check(book_id):
    copies_id = [i for i in BookCopies.select().where(BookCopies.book_id == book_id)]
    for id in copies_id:
        if id.available:
            return True
    return False


def borrow_book(title, student_id):
    try:
        book_id = Book.get(Book.title == title).id
    except Book.DoesNotExist:
        return False
    if book_id:
        if available_check(book_id) and check_student_borrow(book_id, student_id):
            copies_id = BookCopies.get(BookCopies.book_id == book_id, BookCopies.available == True)
            copies_id.available = False
            copies_id.save()
            Borrows.create(book_copy_id=copies_id, student_id=student_id, borrow_date=today)
            return True
    return False


def book_return(title, student_id):
    try:
        book_id = Book.get(Book.title == title).id
    except Book.DoesNotExist:
        return False
    copies_id = [i for i in BookCopies.select().where(BookCopies.book_id == book_id, BookCopies.available == False)]
    for id in copies_id:
        try:
            date = Borrows.get(Borrows.book_copy_id == id, Borrows.student_id == student_id)
            date.return_date = today
            id.available = True
            id.save()
            date.save()
            return True
        except Borrows.DoesNotExist:
            return False


def check_student_borrow(book_id, student_id):
    copies = [i for i in BookCopies.select().where(BookCopies.book_id == book_id, BookCopies.available == False)]
    for i in copies:
        try:
            Borrows.get(Borrows.book_copy_id == i, Borrows.student_id == student_id)
            return False
        except Borrows.DoesNotExist:
            pass
    return True


def student_books(student_id):
    copies = Borrows.select().where(Borrows.student_id == student_id)
    book_ids = [copy.book_copy_id for copy in copies]
    books = [Book.get(Book.id == i.book_id) for i in book_ids]
    return books


def author_books(author_id):
    books_id = BookAuthor.select().where(BookAuthor.author_id == author_id)
    books = [Book.get(Book.id == i.book_id) for i in books_id]
    return books
