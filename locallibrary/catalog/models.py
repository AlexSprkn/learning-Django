from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
	name = models.CharField("Жанр", max_length=200)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "жанр"
		verbose_name_plural = "жанры"


class Language(models.Model):
	name = models.CharField("Название", max_length=200)
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "язык"
		verbose_name_plural = "языки"

class Book(models.Model):
	title = models.CharField("Название", max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name="Автор")
	summary = models.TextField("Краткое описание", max_length=1000, help_text='Введите краткое описание книги')
	isbn = models.CharField('ISBN', max_length=13,
		help_text='Номер <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a> из 13 символов')
	genre = models.ManyToManyField(Genre, help_text='Выберите жанр книги', verbose_name="Жанр")
	language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name="Язык")

	class Meta:
		ordering = ['title']
		verbose_name = "книга"
		verbose_name_plural = "книги"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		return ', '.join([genre.name for genre in self.genre.all()[:3]])
	display_genre.short_description = 'Жанр'


class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
		help_text='Unique ID for this book across the whole library')
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name="Книга")
	imprint = models.CharField("Печать", max_length=200)
	due_back = models.DateField("Дата возврата", null=True, blank=True)
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Читатель")

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		else:
			return False

	LOAN_STATUS = (
		('m', 'Техническое обслуживание'),
		('o', 'У читателя'),
		('a', 'Доступна'),
		('r', 'В резерве'),
		)

	status = models.CharField("Статус", max_length=1, choices=LOAN_STATUS, blank=True,
		default='m', help_text='Статус доступности книги')

	class Meta:
		ordering = ['due_back']
		permissions = (('can_mark_returned', 'Set book as returned'),)
		verbose_name = "экземпляр книги"
		verbose_name_plural = "экземпляры книг"

	def __str__(self):
		return f'{self.id} {self.book.title}'


class Author(models.Model):
	first_name = models.CharField("Имя", max_length=100)
	last_name = models.CharField("Фамилия", max_length=100)
	date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
	date_of_death = models.DateField("Дата смерти", null=True, blank=True)

	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

	class Meta:
		ordering = ['last_name']
		verbose_name = "автор"
		verbose_name_plural = "авторы"
