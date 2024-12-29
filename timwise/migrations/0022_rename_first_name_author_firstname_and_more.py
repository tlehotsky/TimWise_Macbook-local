# Generated by Django 5.0 on 2024-11-30 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timwise', '0021_alter_book_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='full_name',
            new_name='fullname',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='chapter_count',
            new_name='chaptercount',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='year_written',
            new_name='yearwritten',
        ),
    ]
