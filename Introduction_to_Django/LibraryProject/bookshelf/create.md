# CREATE Operation Documentation

## Command
```bash
python manage.py shell -c "from bookshelf.models import Book; book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949); print(f'Created book: {book}'); print(f'Book ID: {book.id}')"
```

## Output
```
7 objects imported automatically (use -v 2 for details).

Created book: 1984 by George Orwell (1949)
Book ID: 1
```

## Explanation
- **Operation**: CREATE
- **Method**: `Book.objects.create()`
- **Book Details**:
  - Title: "1984"
  - Author: "George Orwell"
  - Publication Year: 1949
- **Result**: Book successfully created with ID 1
- **String Representation**: "1984 by George Orwell (1949)" (from the `__str__` method)
