from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer


class BookListCreate(generics.ListCreateAPIView):
    """
    Generic view for listing all books and creating new books.

    Handles:
    - GET /books/: Returns a list of all books (accessible to all users)
    - POST /books/: Creates a new book (requires authentication)

    Permissions:
    - Uses IsAuthenticatedOrReadOnly permission class
    - Unauthenticated users can read (GET) but cannot create (POST)
    - Authenticated users can both read and create

    View Configuration:
    - Uses ListCreateAPIView which combines ListAPIView and CreateAPIView
    - Automatically handles both listing and creation endpoints
    - Serializer handles data validation and serialization
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting a single book.

    Handles:
    - GET /books/<int:pk>/: Retrieves a specific book by primary key
    - PUT /books/<int:pk>/: Updates a specific book (requires authentication)
    - PATCH /books/<int:pk>/: Partially updates a specific book (requires authentication)
    - DELETE /books/<int:pk>/: Deletes a specific book (requires authentication)

    Permissions:
    - Uses IsAuthenticatedOrReadOnly permission class
    - Unauthenticated users can read (GET) individual books
    - Authenticated users can read, update (PUT/PATCH), and delete (DELETE)

    View Configuration:
    - Uses RetrieveUpdateDestroyAPIView which combines:
      * RetrieveAPIView (for GET requests)
      * UpdateAPIView (for PUT/PATCH requests)
      * DestroyAPIView (for DELETE requests)
    - Primary key (pk) is used to identify the specific book instance
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
