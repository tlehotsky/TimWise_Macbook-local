# Generated by Django 5.0 on 2024-11-03 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timwise', '0011_remove_files_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-11-01'),
            preserve_default=False,
        ),
    ]
