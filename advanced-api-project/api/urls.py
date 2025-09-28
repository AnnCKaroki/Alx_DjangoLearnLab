from django.urls import path
from .views import BookListCreate, BookRetrieveUpdateDestroy

urlpatterns = [
    # Book list and creation endpoint
    # GET /books/ - List all books (accessible to all users)
    # POST /books/ - Create a new book (requires authentication)
    path('books/', BookListCreate.as_view(), name='book-list-create'),

    # Book detail, update, and delete endpoint
    # GET /books/<int:pk>/ - Retrieve a specific book (accessible to all users)
    # PUT /books/<int:pk>/ - Update a specific book (requires authentication)
    # PATCH /books/<int:pk>/ - Partially update a specific book (requires authentication)
    # DELETE /books/<int:pk>/ - Delete a specific book (requires authentication)
    path('books/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-detail'),
]
