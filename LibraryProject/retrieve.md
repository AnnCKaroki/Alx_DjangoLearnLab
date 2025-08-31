# RETRIEVE Operation Documentation

## Command
```bash
python manage.py shell -c "from bookshelf.models import Book; book = Book.objects.get(title='1984'); print(f'Retrieved book: {book}'); print(f'Book details - Title: {book.title}, Author: {book.author}, Year: {book.publication_year}')"
```

## Output
```
7 objects imported automatically (use -v 2 for details).

Retrieved book: 1984 by George Orwell (1949)
Book details - Title: 1984, Author: George Orwell, Year: 1949
```

## Explanation
- **Operation**: RETRIEVE
- **Method**: `Book.objects.get(title='1984')`
- **Query**: Retrieve book with title "1984"
- **Result**: Successfully retrieved the book instance
- **Book Details Retrieved**:
  - Title: "1984"
  - Author: "George Orwell"
  - Publication Year: 1949
- **String Representation**: "1984 by George Orwell (1949)"
