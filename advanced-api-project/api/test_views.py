from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BookAPITestCase(APITestCase):
    """
    Comprehensive unit tests for the Book API endpoints.

    Testing Strategy:
    1. CRUD Operations: Verify all Create, Read, Update, Delete operations work correctly
    2. Permissions: Ensure proper access control for authenticated vs unauthenticated users
    3. Validation: Test custom serializer validation (future publication year)
    4. Querying: Test filtering, searching, and ordering functionality

    Test Data Setup:
    - Creates multiple authors and books with varied data for comprehensive testing
    - Sets up both authenticated and unauthenticated test clients
    """

    def setUp(self):
        """
        Set up test data and clients for all test methods.

        Creates:
        - Test user for authentication
        - Multiple authors and books for comprehensive testing
        - Authenticated and unauthenticated API clients
        """
        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create authors
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='Stephen King')
        self.author3 = Author.objects.create(name='Agatha Christie')

        # Create books with varied data for testing
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Shining',
            publication_year=1977,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Murder on the Orient Express',
            publication_year=1934,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='It',
            publication_year=1986,
            author=self.author2
        )

        # Set up API clients
        self.client = APIClient()  # Unauthenticated client
        self.auth_client = APIClient()  # Authenticated client
        self.auth_client.force_authenticate(user=self.user)

        # API endpoints
        self.books_url = reverse('book-list-create')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

    # ==================== CRUD OPERATIONS TESTS ====================

    def test_get_books_list(self):
        """Test GET /books/ - List all books (accessible to all users)"""
        response = self.client.get(self.books_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all 4 books

        # Verify data structure and ordering (should be ordered by publication_year, title)
        books = response.data
        self.assertEqual(books[0]['title'], 'Murder on the Orient Express')  # 1934
        self.assertEqual(books[1]['title'], 'The Hobbit')  # 1937
        self.assertEqual(books[2]['title'], 'The Shining')  # 1977
        self.assertEqual(books[3]['title'], 'It')  # 1986

    def test_get_book_detail(self):
        """Test GET /books/<pk>/ - Retrieve specific book (accessible to all users)"""
        response = self.client.get(self.book_detail_url(self.book1.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
        self.assertEqual(response.data['publication_year'], 1937)
        self.assertEqual(response.data['author'], self.author1.pk)

    def test_create_book_authenticated(self):
        """Test POST /books/ - Create book (requires authentication)"""
        data = {
            'title': 'New Fantasy Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.auth_client.post(self.books_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Fantasy Book')

        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Fantasy Book').exists())

    def test_update_book_authenticated(self):
        """Test PUT /books/<pk>/ - Update book (requires authentication)"""
        data = {
            'title': 'Updated Hobbit Title',
            'publication_year': 1937,
            'author': self.author1.pk
        }
        response = self.auth_client.put(self.book_detail_url(self.book1.pk), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Hobbit Title')

        # Verify book was actually updated in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Hobbit Title')

    def test_partial_update_book_authenticated(self):
        """Test PATCH /books/<pk>/ - Partial update book (requires authentication)"""
        data = {'title': 'Partially Updated Title'}
        response = self.auth_client.patch(self.book_detail_url(self.book1.pk), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Title')
        # Year and author should remain unchanged
        self.assertEqual(response.data['publication_year'], 1937)
        self.assertEqual(response.data['author'], self.author1.pk)

    def test_delete_book_authenticated(self):
        """Test DELETE /books/<pk>/ - Delete book (requires authentication)"""
        book_pk = self.book1.pk
        response = self.auth_client.delete(self.book_detail_url(book_pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(pk=book_pk).exists())

    # ==================== PERMISSIONS TESTS ====================

    def test_create_book_unauthenticated_fails(self):
        """Test POST /books/ - Unauthenticated user cannot create book (should return 401/403)"""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(self.books_url, data)

        # Should return 401 Unauthorized or 403 Forbidden
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_unauthenticated_fails(self):
        """Test PUT /books/<pk>/ - Unauthenticated user cannot update book"""
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1937,
            'author': self.author1.pk
        }
        response = self.client.put(self.book_detail_url(self.book1.pk), data)

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_unauthenticated_fails(self):
        """Test DELETE /books/<pk>/ - Unauthenticated user cannot delete book"""
        response = self.client.delete(self.book_detail_url(self.book1.pk))

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_get_operations_unauthenticated_success(self):
        """Test that unauthenticated users can perform GET operations (read-only access)"""
        # Test list view
        list_response = self.client.get(self.books_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        # Test detail view
        detail_response = self.client.get(self.book_detail_url(self.book1.pk))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    # ==================== VALIDATION TESTS ====================

    def test_create_book_future_year_validation_fails(self):
        """Test custom validation - creating book with future publication year should fail with 400"""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.auth_client.post(self.books_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('future', str(response.data['publication_year'][0]).lower())

    def test_update_book_future_year_validation_fails(self):
        """Test custom validation - updating book with future publication year should fail"""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Updated Title',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.auth_client.put(self.book_detail_url(self.book1.pk), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_create_book_current_year_validation_passes(self):
        """Test that current year is acceptable for publication_year"""
        current_year = datetime.now().year
        data = {
            'title': 'Current Year Book',
            'publication_year': current_year,
            'author': self.author1.pk
        }
        response = self.auth_client.post(self.books_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ==================== QUERYING TESTS ====================

    def test_filter_by_publication_year(self):
        """Test filtering by publication_year query parameter"""
        response = self.client.get(self.books_url, {'publication_year': 1977})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Shining')

    def test_filter_by_author_name(self):
        """Test filtering by author name query parameter"""
        response = self.client.get(self.books_url, {'author__name': 'Stephen King'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 'The Shining' and 'It'
        titles = [book['title'] for book in response.data]
        self.assertIn('The Shining', titles)
        self.assertIn('It', titles)

    def test_filter_by_title(self):
        """Test filtering by exact title"""
        response = self.client.get(self.books_url, {'title': 'The Hobbit'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_search_functionality(self):
        """Test search functionality across title and author name"""
        # Search for 'king' should find books by Stephen King
        response = self.client.get(self.books_url, {'search': 'king'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should find Stephen King's books

        # Search in title
        response = self.client.get(self.books_url, {'search': 'hobbit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_ordering_by_title_ascending(self):
        """Test ordering by title (ascending)"""
        response = self.client.get(self.books_url, {'ordering': 'title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        expected_order = ['It', 'Murder on the Orient Express', 'The Hobbit', 'The Shining']
        self.assertEqual(titles, expected_order)

    def test_ordering_by_title_descending(self):
        """Test ordering by title (descending)"""
        response = self.client.get(self.books_url, {'ordering': '-title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        expected_order = ['The Shining', 'The Hobbit', 'Murder on the Orient Express', 'It']
        self.assertEqual(titles, expected_order)

    def test_ordering_by_publication_year_descending(self):
        """Test ordering by publication_year (descending) - newest first"""
        response = self.client.get(self.books_url, {'ordering': '-publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        expected_order = [1986, 1977, 1937, 1934]  # Newest to oldest
        self.assertEqual(years, expected_order)

        # Verify first book is the newest (It - 1986)
        self.assertEqual(response.data[0]['title'], 'It')

    def test_multiple_ordering(self):
        """Test multiple field ordering"""
        response = self.client.get(self.books_url, {'ordering': 'publication_year,title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by year first, then by title within same year
        expected_titles = ['Murder on the Orient Express', 'The Hobbit', 'The Shining', 'It']
        actual_titles = [book['title'] for book in response.data]
        self.assertEqual(actual_titles, expected_titles)

    def test_combined_query_parameters(self):
        """Test combining filtering, searching, and ordering"""
        # Filter Stephen King's books and order by year descending
        response = self.client.get(self.books_url, {
            'author__name': 'Stephen King',
            'ordering': '-publication_year'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should return 'It' first (1986), then 'The Shining' (1977)
        self.assertEqual(response.data[0]['title'], 'It')
        self.assertEqual(response.data[1]['title'], 'The Shining')

    def test_search_with_ordering(self):
        """Test search combined with ordering"""
        # Search for books with 'The' in title, ordered by year
        response = self.client.get(self.books_url, {
            'search': 'The',
            'ordering': 'publication_year'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)  # Should find multiple books with 'The'

        # Verify ordering by year
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))  # Should be in ascending order

    # ==================== EDGE CASES AND ERROR HANDLING ====================

    def test_nonexistent_book_detail_returns_404(self):
        """Test accessing non-existent book returns 404"""
        response = self.client.get(self.book_detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_filter_values(self):
        """Test that invalid filter values are handled gracefully"""
        # Test with non-existent author name (string field - no conversion error)
        response = self.client.get(self.books_url, {'author__name': 'Nonexistent Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return empty list

        # Test with non-existent title
        response = self.client.get(self.books_url, {'title': 'Nonexistent Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return empty list

    def test_empty_search_returns_all(self):
        """Test that empty search parameter returns all books"""
        response = self.client.get(self.books_url, {'search': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all books
