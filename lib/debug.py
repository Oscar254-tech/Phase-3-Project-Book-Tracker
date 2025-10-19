from db.models import Book, Review, initialize_database

def debug_database():
    """Debug function to show all database contents"""
    initialize_database()
    
    print("🔍 DEBUG DATABASE CONTENTS")
    print("=" * 50)
    
    # Show all books
    books = Book.get_all()
    print(f"\nBOOKS ({len(books)} total):")
    for book in books:
        print(f"  {book.id}: {book.title} by {book.author} | {book.status}")
    
    # Show all reviews
    reviews = Review.get_all()
    print(f"\nREVIEWS ({len(reviews)} total):")
    for review in reviews:
        book = Book.find_by_id(review.book_id)
        book_title = book.title if book else "Unknown"
        print(f"  {review.id}: ⭐{review.rating} for '{book_title}' - '{review.content}'")
    
    # Show relationships
    print(f"\nBOOK-REVIEW RELATIONSHIPS:")
    for book in books:
        book_reviews = book.reviews()
        print(f"  '{book.title}': {len(book_reviews)} reviews")

if __name__ == "__main__":
    debug_database()