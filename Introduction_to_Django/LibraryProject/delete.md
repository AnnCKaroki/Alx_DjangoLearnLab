# DELETE Operation Documentation

## Command
```bash
python manage.py shell -c "from bookshelf.models import Book; book = Book.objects.get(title='Nineteen Eighty-Four'); print(f'Book to delete: {book}'); book.delete(); print('Book deleted successfully')"
```

## Output
```
7 objects imported automatically (use -v 2 for details).

Book to delete: Nineteen Eighty-Four by George Orwell (1949)
Book deleted successfully
```

## Verification Command
```bash
python manage.py shell -c "from bookshelf.models import Book; print('Total books in database:', Book.objects.count())"
```

## Verification Output
```
7 objects imported automatically (use -v 2 for details).

Total books in database: 0
```

## Explanation
- **Operation**: DELETE
- **Method**: 
  1. `Book.objects.get(title='Nineteen Eighty-Four')` - Retrieve the book to delete
  2. `book.delete()` - Delete the book from database
- **Book Deleted**: "Nineteen Eighty-Four by George Orwell (1949)"
- **Result**: Book successfully deleted from database
- **Verification**: Database count shows 0 books, confirming deletion
- **Confirmation**: The book can no longer be retrieved, proving successful deletion
