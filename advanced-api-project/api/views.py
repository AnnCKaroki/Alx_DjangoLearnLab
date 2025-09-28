from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookListCreate(generics.ListCreateAPIView):
    """
    Generic view for listing all books and creating new books with advanced querying capabilities.

    Handles:
    - GET /books/: Returns a list of all books (accessible to all users)
    - POST /books/: Creates a new book (requires authentication)

    Advanced Query Features:

    1. FILTERING (DjangoFilterBackend):
       - Filter by title: ?title=exact_title
       - Filter by author name: ?author__name=author_name
       - Filter by publication year: ?publication_year=2023
       - Multiple filters can be combined: ?publication_year=2023&author__name=John

    2. SEARCHING (SearchFilter):
       - Search across title and author name: ?search=fiction
       - Performs case-insensitive partial matching
       - Searches in both book title and related author's name
       - Example: ?search=tolkien (finds books by Tolkien or with "tolkien" in title)

    3. ORDERING (OrderingFilter):
       - Order by title: ?ordering=title (ascending) or ?ordering=-title (descending)
       - Order by publication year: ?ordering=publication_year or ?ordering=-publication_year
       - Multiple ordering: ?ordering=publication_year,title
       - Default ordering follows model's Meta.ordering

    Combined Query Examples:
    - ?publication_year=2023&search=fiction&ordering=-title
    - ?author__name=Stephen King&ordering=publication_year
    - ?search=fantasy&ordering=-publication_year

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

    # Configure filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Configure filtering fields
    # Allows exact matching on these fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Configure search fields
    # Allows partial, case-insensitive searching across these fields
    search_fields = ['title', 'author__name']

    # Configure ordering fields
    # Allows ordering by these fields (use - prefix for descending order)
    ordering_fields = ['title', 'publication_year']

    # Default ordering when no ordering is specified
    ordering = ['publication_year', 'title']


class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting a single book.

    Handles:
    - GET /books/<int:pk>/: Retrieves a specific book by primary key
    - PUT /books/<int:pk>/: Updates a specific book (requires authentication)
    - PATCH /books/<int:pk>/: Partially updates a specific book (requires authentication)
    - DELETE /books/<int:pk>/: Deletes a specific book (requires authentication)

    Note: Filtering, searching, and ordering are not applicable to single-item endpoints
    as they operate on collections of items.

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
