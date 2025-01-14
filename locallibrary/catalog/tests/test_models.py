from django.test import TestCase

from catalog.models import Genre, Author

class GenreModelsTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		Genre.objects.create(name='Психология')

	def test_name_label(self):
		genre = Genre.objects.get(id=1)
		field_label = genre._meta.get_field('name').verbose_name
		self.assertEquals(field_label, 'Жанр')

	def test_name_max_lenght(self):
		genre = Genre.objects.get(id=1)
		max_length = genre._meta.get_field('name').max_length
		self.assertEquals(max_length, 200)

	def test_class_verbose_name(self):
		genre = Genre.objects.get(id=1)
		verbose_name = genre._meta.verbose_name
		self.assertEquals(verbose_name, 'жанр')


class AuthorModelsTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		Author.objects.create(first_name='Big', last_name='Bob')

	def test_first_name_label(self):
		author = Author.objects.get(id=1)
		field_label = author._meta.get_field('first_name').verbose_name
		self.assertEquals(field_label, 'Имя')

	def test_last_name_label(self):
		author = Author.objects.get(id=1)
		field_label = author._meta.get_field('last_name').verbose_name
		self.assertEquals(field_label, 'Фамилия')

	def test_date_of_birth_label(self):
		author = Author.objects.get(id=1)
		field_label = author._meta.get_field('date_of_birth').verbose_name
		self.assertEquals(field_label, 'Дата рождения')

	def test_date_of_death_label(self):
		author = Author.objects.get(id=1)
		field_label = author._meta.get_field('date_of_death').verbose_name
		self.assertEquals(field_label, 'Дата смерти')

	def test_first_name_max_lenght(self):
		author = Author.objects.get(id=1)
		max_length = author._meta.get_field('first_name').max_length
		self.assertEquals(max_length,100)

	def test_last_name_max_lenght(self):
		author = Author.objects.get(id=1)
		max_length = author._meta.get_field('last_name').max_length
		self.assertEquals(max_length,100)

	def test_object_name_is_last_name_comma_first_name(self):
		author = Author.objects.get(id=1)
		expected_object_name = f'{author.last_name}, {author.first_name}'
		self.assertEquals(expected_object_name, str(author))

	def test_get_absolute_url(self):
		author = Author.objects.get(id=1)
		self.assertEquals(author.get_absolute_url(), '/catalog/author/1')