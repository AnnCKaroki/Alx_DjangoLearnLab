from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.

    Fields:
    - name: The full name of the author (CharField with max 100 characters)

    This model has a one-to-many relationship with Book model.
    One author can write multiple books.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a book in the library.

    Fields:
    - title: The title of the book (CharField with max 200 characters)
    - publication_year: The year the book was published (IntegerField)
    - author: Foreign key relationship to Author model (many-to-one)

    Relationships:
    - Each book belongs to one author (many-to-one relationship via ForeignKey)
    - When an author is deleted, all their books are also deleted (CASCADE)
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ['publication_year', 'title']
