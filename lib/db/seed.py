from models import Book, Review, initialize_database

def seed_database():
    """Seed the database with sample data"""
    initialize_database()
    
    # Clear existing data
    Book.CURSOR.execute("DELETE FROM reviews")
    Book.CURSOR.execute("DELETE FROM books")
    Book.CONN.commit()

    # Create sample books
    books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", "completed"),
        Book("Dune", "Frank Herbert", "Science Fiction", "reading"),
        Book("To Kill a Mockingbird", "Harper Lee", "Classic", "completed"),
        Book("Project Hail Mary", "Andy Weir", "Science Fiction", "want_to_read"),
        Book("1984", "George Orwell", "Dystopian", "completed")
    ]

    for book in books:
        book.save()

    # Create sample reviews
    reviews = [
        Review("A masterpiece of American literature", 5, 1),
        Review("Complex characters and beautiful prose", 4, 1),
        Review("Epic sci-fi world building", 5, 2),
        Review("A powerful story about justice and morality", 5, 3),
        Review("Thought-provoking and brilliantly written", 4, 5)
    ]

    for review in reviews:
        review.save()

    print("Database seeded successfully!")
    print(f"Created {len(books)} books and {len(reviews)} reviews")

if __name__ == "__main__":
    seed_database()