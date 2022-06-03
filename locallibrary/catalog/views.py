from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
	#Функция для отображения домашней страницы сайта
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()
	num_genres = Genre.objects.count()
	# Количество книг про Шерлока Холмса
	num_holmes = Book.objects.filter(title__contains='Шерлок').filter(title__contains='Холмс').count()
	# Количество посещений
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	return render(
		request,
		'index.html',
		context = {'num_books' : num_books, 'num_instances' : num_instances,
		'num_instances_available' : num_instances_available, 'num_authors' : num_authors,
		'num_genres' : num_genres, 'num_holmes' : num_holmes, 'num_visits':num_visits},
		)

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10

    # def queryset(self):
    # 	return Book.objects.order_by('title')

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorDetailView(generic.DetailView):
	model = Author
	template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = ('catalog.can_mark_returned')
	template_name = 'all_borrowed.html'
	#paginate_by = 10

	def queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')