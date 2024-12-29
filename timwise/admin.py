from django.contrib import admin
from .models import Book, Author, Highlight, Files


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('ID', 'lastname', 'firstname', 'fullname')  # Assuming fields are 'last_name' and 'first_name'

class BookAdmin(admin.ModelAdmin):
    list_display = ('ID', 'name', 'chaptercount', 'yearwritten')

class HighlightAdmin(admin.ModelAdmin):
    list_display = ('ID', 'book', 'chapter_number', 'html_line_number', 'color', 'page_number', 'text')

class FilesAdmin(admin.ModelAdmin):
    list_display = ('file',)  


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Highlight, HighlightAdmin)
admin.site.register(Files, FilesAdmin)















####### leave this commented out


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('ID', 'name', 'authortemp', 'chaptercount', 'year_written')




































