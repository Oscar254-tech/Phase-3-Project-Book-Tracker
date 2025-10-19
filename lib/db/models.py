import sqlite3

# Database connection
CONN = sqlite3.connect('lib/db/book_tracker.db')
CURSOR = CONN.cursor()

class Book:
    def __init__(self, title, author, genre=None, status="want_to_read", id=None):
        self.id = id
        self.genre = genre
        self._reviews = []
        
        # Initialize private attributes first
        self._title = None
        self._author = None
        self._status = None
        
        # Use property setters for validation
        self.title = title
        self.author = author
        self.status = status

    def __repr__(self):
        return f"<Book {self.id}: {self.title} by {self.author}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Author cannot be empty")
        if len(value) > 50:
            raise ValueError("Author name cannot exceed 50 characters")
        self._author = value.strip()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ['want_to_read', 'reading', 'completed']
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        self._status = value

    # ORM Methods
    def save(self):
        """Create a new book in the database"""
        try:
            CURSOR.execute('''
                INSERT INTO books (title, author, genre, status)
                VALUES (?, ?, ?, ?)
            ''', (self.title, self.author, self.genre, self.status))
            CONN.commit()
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Database error: {e}")

    def update(self):
        """Update an existing book in the database"""
        if not self.id:
            raise ValueError("Book must have an ID to update")
        
        CURSOR.execute('''
            UPDATE books 
            SET title=?, author=?, genre=?, status=?
            WHERE id=?
        ''', (self.title, self.author, self.genre, self.status, self.id))
        CONN.commit()
        return self

    def delete(self):
        """Delete the book from the database"""
        if not self.id:
            raise ValueError("Book must have an ID to delete")
        
        # First delete associated reviews (maintain referential integrity)
        CURSOR.execute("DELETE FROM reviews WHERE book_id=?", (self.id,))
        CURSOR.execute("DELETE FROM books WHERE id=?", (self.id,))
        CONN.commit()

    # Class Methods
    @classmethod
    def create_table(cls):
        """Create the books table"""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                status TEXT DEFAULT 'want_to_read'
            )
        ''')
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Get all books from the database"""
        rows = CURSOR.execute("SELECT * FROM books").fetchall()
        books = []
        for row in rows:
            book = cls(
                id=row[0],
                title=row[1],
                author=row[2],
                genre=row[3],
                status=row[4]
            )
            books.append(book)
        return books

    @classmethod
    def find_by_id(cls, book_id):
        """Find a book by ID"""
        row = CURSOR.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
        if row:
            return cls(
                id=row[0],
                title=row[1],
                author=row[2],
                genre=row[3],
                status=row[4]
            )
        return None

    @classmethod
    def find_by_title(cls, title):
        """Find books by title (partial match)"""
        rows = CURSOR.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{title}%',)).fetchall()
        books = []
        for row in rows:
            book = cls(
                id=row[0],
                title=row[1],
                author=row[2],
                genre=row[3],
                status=row[4]
            )
            books.append(book)
        return books

    @classmethod
    def find_by_author(cls, author):
        """Find books by author (partial match)"""
        rows = CURSOR.execute("SELECT * FROM books WHERE author LIKE ?", (f'%{author}%',)).fetchall()
        books = []
        for row in rows:
            book = cls(
                id=row[0],
                title=row[1],
                author=row[2],
                genre=row[3],
                status=row[4]
            )
            books.append(book)
        return books

    @classmethod
    def find_by_status(cls, status):
        """Find books by reading status"""
        rows = CURSOR.execute("SELECT * FROM books WHERE status=?", (status,)).fetchall()
        books = []
        for row in rows:
            book = cls(
                id=row[0],
                title=row[1],
                author=row[2],
                genre=row[3],
                status=row[4]
            )
            books.append(book)
        return books

    # Relationship Methods - FIXED: Removed circular imports
    def reviews(self):
        """Get all reviews for this book"""
        # Use Review class directly since it's in the same file
        return Review.find_by_book_id(self.id)

    def add_review(self, content, rating):
        """Add a review to this book"""
        # Use Review class directly since it's in the same file
        review = Review(content, rating, self.id)
        return review.save()


class Review:
    def __init__(self, content, rating, book_id, id=None):
        self.id = id
        # Initialize private attributes first
        self._content = None
        self._rating = None
        self._book_id = None
        
        # Use property setters for validation
        self.content = content
        self.rating = rating
        self.book_id = book_id

    def __repr__(self):
        return f"<Review {self.id}: {self.rating} stars for book {self.book_id}>"

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Review content cannot be empty")
        if len(value) > 500:
            raise ValueError("Review content cannot exceed 500 characters")
        self._content = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    @property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def book_id(self, value):
        if not value:
            raise ValueError("Review must be associated with a book")
        self._book_id = value

    # ORM Methods
    def save(self):
        """Create a new review in the database"""
        try:
            CURSOR.execute('''
                INSERT INTO reviews (content, rating, book_id)
                VALUES (?, ?, ?)
            ''', (self.content, self.rating, self.book_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Database error: {e}")

    def update(self):
        """Update an existing review in the database"""
        if not self.id:
            raise ValueError("Review must have an ID to update")
        
        CURSOR.execute('''
            UPDATE reviews 
            SET content=?, rating=?, book_id=?
            WHERE id=?
        ''', (self.content, self.rating, self.book_id, self.id))
        CONN.commit()
        return self

    def delete(self):
        """Delete the review from the database"""
        if not self.id:
            raise ValueError("Review must have an ID to delete")
        
        CURSOR.execute("DELETE FROM reviews WHERE id=?", (self.id,))
        CONN.commit()

    # Class Methods
    @classmethod
    def create_table(cls):
        """Create the reviews table"""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                rating INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        ''')
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Get all reviews from the database"""
        rows = CURSOR.execute("SELECT * FROM reviews").fetchall()
        reviews = []
        for row in rows:
            review = cls(
                id=row[0],
                content=row[1],
                rating=row[2],
                book_id=row[3]
            )
            reviews.append(review)
        return reviews

    @classmethod
    def find_by_id(cls, review_id):
        """Find a review by ID"""
        row = CURSOR.execute("SELECT * FROM reviews WHERE id=?", (review_id,)).fetchone()
        if row:
            return cls(
                id=row[0],
                content=row[1],
                rating=row[2],
                book_id=row[3]
            )
        return None

    @classmethod
    def find_by_book_id(cls, book_id):
        """Find all reviews for a specific book"""
        rows = CURSOR.execute("SELECT * FROM reviews WHERE book_id=?", (book_id,)).fetchall()
        reviews = []
        for row in rows:
            review = cls(
                id=row[0],
                content=row[1],
                rating=row[2],
                book_id=row[3]
            )
            reviews.append(review)
        return reviews

    @classmethod
    def find_by_rating(cls, rating):
        """Find reviews by rating"""
        rows = CURSOR.execute("SELECT * FROM reviews WHERE rating=?", (rating,)).fetchall()
        reviews = []
        for row in rows:
            review = cls(
                id=row[0],
                content=row[1],
                rating=row[2],
                book_id=row[3]
            )
            reviews.append(review)
        return reviews


# Initialize database tables
def initialize_database():
    Book.create_table()
    Review.create_table()