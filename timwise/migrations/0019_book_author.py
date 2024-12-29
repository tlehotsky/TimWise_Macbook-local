# Generated by Django 5.0 on 2024-11-30 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timwise', '0018_remove_book_authortemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='timwise.author', verbose_name='book author'),
        ),
    ]
