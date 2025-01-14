from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm

#Для редактирования класса Author
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Для листания списка книг у читателей
from django.core.paginator import Paginator



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


@login_required
@permission_required('catalog.can_mark_returned')
def all_borrowed_books(request):
	borrowed_books = BookInstance.objects.filter(status__exact='o').order_by('due_back')
	paginate_by = 10
	paginator = Paginator(borrowed_books, paginate_by)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	is_paginated = paginator.count > paginate_by
	return render(
		request,
		'all_borrowed.html',
		{'page_obj': page_obj, 'is_paginated': is_paginated}
		)

@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_inst = get_object_or_404(BookInstance, pk=pk)

	if request.method == 'POST':

		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()

			return HttpResponseRedirect(reverse('all-borrowed'))

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)

		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

	return render(request, 'book_renew_librarian.html', {'form': form, 'book_inst':book_inst})

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	model = Author
	permission_required = ('catalog.can_mark_returned')
	fields = '__all__'
	initial = {'date_of_death':'12/10/2016'}

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Author
	permission_required = 'catalog.can_mark_returned'
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Author
	permission_required = 'catalog.can_mark_returned'
	success_url = reverse_lazy('authors')

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	model = Book
	permission_required = 'catalog.can_mark_returned'
	fields = '__all__'

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Book
	permission_required = 'catalog.can_mark_returned'
	fields = '__all__'

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Book
	permission_required = 'catalog.can_mark_returned'
	success_url = reverse_lazy('books')