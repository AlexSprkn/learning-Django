from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookInline(admin.TabularInline):
	model = Book
	extra = 0


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInline]


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BooksInstanceInline]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back')
	fieldsets = (
		(None, {'fields': ('book', 'imprint', 'id')}),
		('Availability', {'fields': ('status', 'due_back', 'borrower')})
		)


admin.site.register(Language)