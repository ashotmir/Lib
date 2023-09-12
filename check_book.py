from models import Book, Author, BookCopies, BookAuthor


class AddBook:
    first_name = None
    second_name = None
    year_first_published = None
    title = None
    quantity = None
    isbn = None
    year_published = None

    @classmethod
    def create_book(cls, form):
        cls.title = form.title.data
        cls.year_first_published = form.year_first_published.data
        cls.first_name = form.first_name.data
        cls.second_name = form.second_name.data
        cls.quantity = form.quantity.data
        cls.isbn = form.isbn.data
        cls.year_published = form.year_published.data

        author = cls.check_author(cls.first_name, cls.second_name)
        book = cls.check_book(cls.title, cls.year_first_published)
        cls.book_author_contact(book=book, author=author)
        cls.add_copies(book_id=book, quantity=cls.quantity, isbn=cls.isbn, year_published=cls.year_published)

    @staticmethod
    def check_author(first_name, second_name):
        try:
            author = Author.get(Author.first_name == first_name, Author.second_name == second_name)
            print(f"Author ID: {author.id} -- {author.first_name}")
            return author.id
        except Author.DoesNotExist:
            new_author = Author.create(first_name=first_name, second_name=second_name)
            print(f"New author created with ID: {new_author.id} -- {new_author.first_name}")
            return new_author.id

    @staticmethod
    def check_book(title, year_first_published):
        try:
            book = Book.get(Book.title == title, Book.year_first_published == year_first_published)
            print(f"Book ID: {book.id} -- {book.title}")
            return book.id
        except Book.DoesNotExist:
            new_book = Book.create(title=title, year_first_published=year_first_published)
            print(f"New book created with ID: {new_book.id} -- {new_book.year_first_published}")
            return new_book.id

    @staticmethod
    def book_author_contact(book, author):
        try:
            BookAuthor.get(book_id=book, author_id=author)
        except BookAuthor.DoesNotExist:
            BookAuthor.create(book_id=book, author_id=author)

    @staticmethod
    def add_copies(book_id, quantity, isbn, year_published):
        for i in range(int(quantity)):
            BookCopies.create(book_id=book_id, ISBN=isbn, year_published=year_published)

