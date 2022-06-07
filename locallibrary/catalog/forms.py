from django import forms

from django.core.exceptions import ValidationError
import datetime

class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="Введите дату между текущей и 4 неделями (по умолчанию 3).", label = 'Обновить дату')

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		if data < datetime.date.today():
			raise ValidationError('Неверная дата возврата - указано прошлое время')

		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError('Неверная дата возврата - указан возврат более чем через 4 недели')

		return data
