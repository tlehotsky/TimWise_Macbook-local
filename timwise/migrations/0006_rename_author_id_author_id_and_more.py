# Generated by Django 5.0 on 2024-10-19 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timwise', '0005_alter_author_author_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author_id',
            new_name='ID',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='author_first_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='author_last_name',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_id',
            new_name='ID',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='bookauthor_ID',
            new_name='authorID',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='bookname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_ID',
            new_name='ID',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_color',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_chapter_number',
            new_name='hapter_number',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_html_line_number',
            new_name='html_line_number',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_page_number',
            new_name='page_number',
        ),
        migrations.RenameField(
            model_name='highlight',
            old_name='highlight_text',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='highlight',
            name='highlight_book_ID',
        ),
        migrations.AddField(
            model_name='highlight',
            name='book_ID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='timwise.book'),
            preserve_default=False,
        ),
    ]
