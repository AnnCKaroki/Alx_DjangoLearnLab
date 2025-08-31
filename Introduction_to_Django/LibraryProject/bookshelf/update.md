# UPDATE Operation Documentation

## Command
```bash
python manage.py shell -c "from bookshelf.models import Book; book = Book.objects.get(title='1984'); print(f'Before update: {book}'); book.title = 'Nineteen Eighty-Four'; book.save(); print(f'After update: {book}')"
```

## Output
```
7 objects imported automatically (use -v 2 for details).

Before update: 1984 by George Orwell (1949)
After update: Nineteen Eighty-Four by George Orwell (1949)
```

## Explanation
- **Operation**: UPDATE
- **Method**: 
  1. `Book.objects.get(title='1984')` - Retrieve the book
  2. `book.title = 'Nineteen Eighty-Four'` - Update the title attribute
  3. `book.save()` - Save the changes to database
- **Change Made**: Title updated from "1984" to "Nineteen Eighty-Four"
- **Before Update**: "1984 by George Orwell (1949)"
- **After Update**: "Nineteen Eighty-Four by George Orwell (1949)"
- **Result**: Book title successfully updated and saved to database
