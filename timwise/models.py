# timwise django app
# timwise.models.py
# 
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now


class Author(models.Model):  
    ID = models.AutoField(primary_key=True, verbose_name="author ID")
    lastname = models.CharField(max_length=30,verbose_name="author last name")
    firstname = models.CharField(max_length=30, verbose_name="author first name")
    fullname = models.CharField(max_length=60, unique=True, verbose_name="author full name")
    dateloaded=models.CharField(max_length=12)
    sessionkey = models.CharField(max_length=50, verbose_name="django session key")
    timestamp=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.fullname

class Book(models.Model): 
    timestamp=models.DateTimeField(auto_now_add=True)
    sessionkey = models.CharField(max_length=50, verbose_name="django session key")
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="book author")
    chaptercount = models.IntegerField(verbose_name="chapter count")
    dateloaded=models.CharField(max_length=12)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    yearwritten = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(9999)], verbose_name="year written"
    )

    class Meta:
        unique_together = ['name', 'author']  # Add this to prevent duplicate books by same author

    def __str__(self):
        return f"{self.name} by {self.author}"


class Highlight(models.Model):  
    ID = models.AutoField(primary_key=True, verbose_name="highlight ID")
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=50)
    html_line_number = models.IntegerField(verbose_name="highlight html line number")
    color = models.CharField(max_length=30, verbose_name="highlight color")
    page_number = models.CharField(max_length=50, verbose_name="highlight page number")
    text = models.TextField(verbose_name="highlight text")
    sessionkey = models.CharField(max_length=50, verbose_name="django session key")
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    dateloaded=models.CharField(max_length=12, verbose_name="date")

class Files(models.Model):
    file=models.FileField(verbose_name="files")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)