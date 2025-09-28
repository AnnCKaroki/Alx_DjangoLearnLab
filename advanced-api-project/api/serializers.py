from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer for serializing Book model instances.

    Serializes all fields of the Book model:
    - title: Book title
    - publication_year: Year of publication
    - author: Foreign key to Author (will show author ID by default)

    Custom Validation:
    - validate_publication_year: Ensures the publication year is not in the future
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation method for publication_year field.

        Ensures that the publication year is not a future year.
        Current year is acceptable, but any year beyond current year will raise a ValidationError.

        Args:
            value (int): The publication year to validate

        Returns:
            int: The validated publication year

        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year

        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )

        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer for serializing Author model instances.

    Fields:
    - name: Author's name
    - books: Nested serialization of all books related to this author

    Nested Relationship Handling:
    The 'books' field uses the BookSerializer to provide a nested representation
    of all books written by this author. This is achieved using the related_name='books'
    defined in the Book model's ForeignKey relationship.

    - many=True: Indicates that one author can have multiple books
    - read_only=True: Makes the books field read-only to prevent modification through this serializer

    This nested approach allows clients to get complete author information including
    all their books in a single API call, reducing the need for multiple requests.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
