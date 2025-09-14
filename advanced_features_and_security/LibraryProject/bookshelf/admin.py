from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo')

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author']
    ordering = ['title']
