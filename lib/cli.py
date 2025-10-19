from helpers import (
    display_main_menu, display_books, display_reviews,
    get_valid_rating, get_valid_book_id, get_valid_review_id, get_book_status
)
from db.models import Book, Review, initialize_database

def add_new_book():
    print("\n➕ ADD NEW BOOK")
    try:
        title = input("Book title: ").strip()
        author = input("Author: ").strip()
        genre = input("Genre (optional): ").strip() or None
        status = get_book_status()
        
        book = Book(title, author, genre, status)
        book.save()
        print(f"✅ '{title}' added successfully with ID: {book.id}")
    except ValueError as e:
        print(f"❌ Error: {e}")

def view_all_books():
    books = Book.get_all()
    display_books(books, "ALL BOOKS")

def find_book_by_id():
    try:
        book_id = get_valid_book_id()
        book = Book.find_by_id(book_id)
        if book:
            display_books([book], f"BOOK #{book.id}")
            # Show reviews for this book
            reviews = book.reviews()
            display_reviews(reviews, f"REVIEWS FOR '{book.title}'")
    except ValueError as e:
        print(f"❌ Error: {e}")

def find_books_by_title():
    title = input("Enter title search term: ").strip()
    books = Book.find_by_title(title)
    display_books(books, f"BOOKS WITH '{title}' IN TITLE")

def find_books_by_author():
    author = input("Enter author search term: ").strip()
    books = Book.find_by_author(author)
    display_books(books, f"BOOKS BY '{author}'")

def update_book_status():
    view_all_books()
    try:
        book_id = get_valid_book_id()
        book = Book.find_by_id(book_id)
        
        if book:
            print(f"\nUpdating status for: {book.title}")
            new_status = get_book_status()
            book.status = new_status
            book.update()
            print("✅ Status updated successfully!")
        else:
            print("Book not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def delete_book():
    view_all_books()
    try:
        book_id = get_valid_book_id()
        book = Book.find_by_id(book_id)
        
        if book:
            confirm = input(f"Are you sure you want to delete '{book.title}' and all its reviews? (y/n): ").strip().lower()
            if confirm == 'y':
                book.delete()
                print("✅ Book and associated reviews deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print("Book not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def add_review_to_book():
    view_all_books()
    try:
        book_id = get_valid_book_id()
        book = Book.find_by_id(book_id)
        
        if book:
            print(f"\nAdding review for: {book.title}")
            content = input("Enter your review: ").strip()
            rating = get_valid_rating()
            
            review = Review(content, rating, book_id)
            review.save()
            print("✅ Review added successfully!")
        else:
            print("Book not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def view_all_reviews():
    reviews = Review.get_all()
    display_reviews(reviews, "ALL REVIEWS")

def find_reviews_by_book():
    view_all_books()
    try:
        book_id = get_valid_book_id()
        book = Book.find_by_id(book_id)
        
        if book:
            reviews = Review.find_by_book_id(book_id)
            display_reviews(reviews, f"REVIEWS FOR '{book.title}'")
        else:
            print("Book not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def find_reviews_by_rating():
    try:
        rating = get_valid_rating()
        reviews = Review.find_by_rating(rating)
        display_reviews(reviews, f"REVIEWS WITH {rating} STARS")
    except ValueError as e:
        print(f"❌ Error: {e}")

def delete_review():
    view_all_reviews()
    try:
        review_id = get_valid_review_id()
        review = Review.find_by_id(review_id)
        
        if review:
            book = Book.find_by_id(review.book_id)
            book_title = book.title if book else "Unknown Book"
            confirm = input(f"Are you sure you want to delete this review for '{book_title}'? (y/n): ").strip().lower()
            if confirm == 'y':
                review.delete()
                print("✅ Review deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print("Review not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def view_reading_statistics():
    books = Book.get_all()
    if not books:
        print("No books in your collection yet.")
        return
    
    total_books = len(books)
    completed = len([b for b in books if b.status == 'completed'])
    reading = len([b for b in books if b.status == 'reading'])
    want_to_read = len([b for b in books if b.status == 'want_to_read'])
    
    all_reviews = Review.get_all()
    avg_rating = sum(review.rating for review in all_reviews) / len(all_reviews) if all_reviews else None
    
    print("\n📊 READING STATISTICS")
    print("=" * 30)
    print(f"Total books: {total_books}")
    print(f"Completed: {completed}")
    print(f"Currently reading: {reading}")
    print(f"Want to read: {want_to_read}")
    print(f"Total reviews: {len(all_reviews)}")
    if avg_rating:
        print(f"Average rating: {avg_rating:.1f} ⭐")
    
    # Books with most reviews
    if all_reviews:
        book_review_counts = {}
        for review in all_reviews:
            book_review_counts[review.book_id] = book_review_counts.get(review.book_id, 0) + 1
        
        if book_review_counts:
            max_reviews = max(book_review_counts.values())
            most_reviewed_books = [Book.find_by_id(book_id) for book_id, count in book_review_counts.items() if count == max_reviews]
            print(f"\nMost reviewed book(s) ({max_reviews} reviews):")
            for book in most_reviewed_books:
                if book:
                    print(f"  - {book.title}")

def main():
    # Initialize database
    initialize_database()
    
    print("📚 Welcome to Your Personal Book Tracker!")
    print("Database initialized successfully!")
    
    while True:
        display_main_menu()
        choice = input("Enter your choice (1-14): ").strip()
        
        try:
            if choice == '1':
                add_new_book()
            elif choice == '2':
                view_all_books()
            elif choice == '3':
                find_book_by_id()
            elif choice == '4':
                find_books_by_title()
            elif choice == '5':
                find_books_by_author()
            elif choice == '6':
                update_book_status()
            elif choice == '7':
                delete_book()
            elif choice == '8':
                add_review_to_book()
            elif choice == '9':
                view_all_reviews()
            elif choice == '10':
                find_reviews_by_book()
            elif choice == '11':
                find_reviews_by_rating()
            elif choice == '12':
                delete_review()
            elif choice == '13':
                view_reading_statistics()
            elif choice == '14':
                print("Happy reading! 📖")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    main()