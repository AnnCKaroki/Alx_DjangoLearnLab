# query_samples.py
# This script demonstrates how to use Django ORM to query relationships

# Import necessary modules
import os
import django

# Set up Django environment
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# Import models
from relationship_app.models import Author, Book, Library, Librarian

# Sample function to create test data
def create_sample_data():
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="Fantastic Beasts", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book2, book3, book4)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="John Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Jane Doe", library=library2)
    
    print("Sample data created successfully!")

# Query 1: Get all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None

# Query 2: List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        
        print(f"\nBooks in {library_name}:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None

# Query 3: Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        
        print(f"\nLibrarian for {library_name}:")
        print(f"- {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
        return None

# Main execution
if __name__ == "__main__":
    # Create sample data (only run once)
    # Uncomment the line below if you need to create sample data again
    # create_sample_data()
    
    # Run sample queries
    get_books_by_author("J.K. Rowling")
    get_books_in_library("Central Library")
    get_librarian_for_library("Community Library")