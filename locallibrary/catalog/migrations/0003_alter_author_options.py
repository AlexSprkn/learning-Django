# Generated by Django 4.0.4 on 2022-05-20 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_book_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]
