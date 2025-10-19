from db.models import Book, Review

def display_main_menu():
    print("\n" + "="*50)
    print("📚 BOOK TRACKER CLI")
    print("="*50)
    print("BOOK MANAGEMENT")
    print("1.  Add New Book")
    print("2.  View All Books")
    print("3.  Find Book by ID")
    print("4.  Find Books by Title")
    print("5.  Find Books by Author")
    print("6.  Update Book Status")
    print("7.  Delete Book")
    print("\nREVIEW MANAGEMENT")
    print("8.  Add Review to Book")
    print("9.  View All Reviews")
    print("10. Find Reviews by Book")
    print("11. Find Reviews by Rating")
    print("12. Delete Review")
    print("\nSTATISTICS")
    print("13. View Reading Statistics")
    print("14. Exit")
    print("="*50)

def display_books(books, title="BOOKS"):
    if not books:
        print(f"No {title.lower()} found.")
        return
    
    print(f"\n📖 {title} ({len(books)} found)")
    print("-" * 60)
    for book in books:
        status_icons = {
            'want_to_read': '📚',
            'reading': '🔖', 
            'completed': '✅'
        }
        print(f"{book.id}. {status_icons[book.status]} {book.title} by {book.author}")
        print(f"   Genre: {book.genre or 'Not specified'} | Status: {book.status.replace('_', ' ').title()}")
        
        # Show reviews for this book
        reviews = book.reviews()
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            print(f"   Reviews: {len(reviews)} | Avg Rating: {avg_rating:.1f} ⭐")
        print()

def display_reviews(reviews, title="REVIEWS"):
    if not reviews:
        print(f"No {title.lower()} found.")
        return
    
    print(f"\n📝 {title} ({len(reviews)} found)")
    print("-" * 50)
    for review in reviews:
        book = Book.find_by_id(review.book_id)
        book_title = book.title if book else "Unknown Book"
        print(f"{review.id}. ⭐ {review.rating}/5 - {book_title}")
        print(f"   {review.content}")
        print()

def get_valid_rating():
    """Get a valid rating from user input"""
    while True:
        try:
            rating = int(input("Enter rating (1-5): "))
            if 1 <= rating <= 5:
                return rating
            else:
                print("Rating must be between 1 and 5")
        except ValueError:
            print("Please enter a valid number")

def get_valid_book_id():
    """Get a valid book ID from user input"""
    while True:
        try:
            book_id = int(input("Enter book ID: "))
            book = Book.find_by_id(book_id)
            if book:
                return book_id
            else:
                print("Book not found. Please enter a valid book ID.")
        except ValueError:
            print("Please enter a valid number")

def get_valid_review_id():
    """Get a valid review ID from user input"""
    while True:
        try:
            review_id = int(input("Enter review ID: "))
            review = Review.find_by_id(review_id)
            if review:
                return review_id
            else:
                print("Review not found. Please enter a valid review ID.")
        except ValueError:
            print("Please enter a valid number")

def get_book_status():
    """Get valid book status from user"""
    print("\nReading Status:")
    print("1. Want to read")
    print("2. Currently reading")
    print("3. Completed")
    
    while True:
        choice = input("Choose status (1-3): ").strip()
        status_map = {'1': 'want_to_read', '2': 'reading', '3': 'completed'}
        if choice in status_map:
            return status_map[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")