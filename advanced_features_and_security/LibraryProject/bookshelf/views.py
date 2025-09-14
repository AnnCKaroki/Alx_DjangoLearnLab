from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def view_page(request):
    return render(request, 'bookshelf/view_page.html')

@permission_required('bookshelf.can_create', raise_exception=True)
def create_page(request):
    return render(request, 'bookshelf/create_page.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_page(request):
    return render(request, 'bookshelf/edit_page.html')

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_page(request):
    return render(request, 'bookshelf/delete_page.html')
