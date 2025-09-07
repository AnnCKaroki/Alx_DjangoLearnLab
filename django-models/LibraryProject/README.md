# LibraryProject

A Django-based library management system for learning Django fundamentals.

## Project Overview

This project demonstrates Django development fundamentals including:
- Setting up a Django environment
- Creating models and performing CRUD operations
- Customizing the Django admin interface

## Technology Stack

- **Language**: Python
- **Framework**: Django
- **Database**: SQLite (default)

## Project Structure

```
LibraryProject/
├── LibraryProject/     # Main project directory
├── bookshelf/         # Django app for book management
├── manage.py          # Django management script
├── README.md          # This file
├── create.md          # CREATE operation documentation
├── retrieve.md        # RETRIEVE operation documentation
├── update.md          # UPDATE operation documentation
└── delete.md          # DELETE operation documentation
```

## Setup Instructions

1. **Install Django**:
   ```bash
   pip install django
   ```

2. **Create the project**:
   ```bash
   python -m django startproject LibraryProject
   ```

3. **Create the app**:
   ```bash
   python manage.py startapp bookshelf
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the admin interface**:
   - URL: http://127.0.0.1:8000/admin/
   - Username: admin
   - Password: admin123

## Features

- Book model with title, author, and publication year fields
- CRUD operations through Django shell
- Customized Django admin interface with:
  - List display showing title, author, and publication year
  - Filtering by publication year and author
  - Search functionality for title and author
  - Automatic ordering by title
- Complete documentation of all operations

## Next Steps

1. Define the Book model in `bookshelf/models.py`
2. Create and apply migrations
3. Perform CRUD operations in Django shell
4. Customize the admin interface
5. Document all operations in separate markdown files

## Verification Checklist

- [x] Project and app created with correct names
- [x] Book model defined with required fields
- [x] Migrations created and applied
- [x] CRUD operations documented
- [x] Admin interface customized
