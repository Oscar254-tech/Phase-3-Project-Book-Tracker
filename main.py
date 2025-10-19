from lib.database import create_tables
from lib.cli import main_menu

def seed_sample_data():
    """Add some sample books for testing"""
    from lib.models.book import Book
    
    sample_books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", "completed", 5, "American classic"),
        Book("Dune", "Frank Herbert", "Science Fiction", "reading", 4),
        Book("Project Hail Mary", "Andy Weir", "Science Fiction", "want_to_read"),
    ]
    
    for book in sample_books:
        try:
            book.save()
            print(f"Added sample book: {book.title}")
        except Exception as e:
            print(f"Note: {book.title} may already exist in database")

if __name__ == "__main__":
    create_tables()     # Set up the database
    seed_sample_data()  # Add sample data
    main_menu()         # Launch the CLI