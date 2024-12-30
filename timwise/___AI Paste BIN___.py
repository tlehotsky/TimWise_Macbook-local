for my timwise django app, I want to create the following:
1. modify the myhighlights.html file to include an additional column labeled 'action'.
2. each row that loads in the myhighlights.html file will a link in the 'action' column that will take the user to a new page called edit_highlight.html
3. when the user clicks on that link in the 'action' column, the user will be taken to the edit_highlight.html page where they can edit the highlight.

please help me modify the myhighlights.html file to include the 'action' column and the link to the edit_highlight.html page and please help me create the edit_highlight.html page.

this is my myhighlights.html file:

<!-- timwise django app
templates.myhighlights.html -->


{% extends 'base.html' %}

{% block title %}My Highlights{% endblock %}

{% block content %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Highlights</title>
    <br>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;  /* Adjust the font size for the entire table */
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            font-size: 12px;  /* Adjust the font size for table headers and data */
        }
        th {
            background-color: #f4f4f4;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
</head>
<body>
    <h1>My Highlights</h1>
    <br>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Book</th>
                <th>Chapter</th>
                <th>Page</th>
                <th>Line Number</th>
                <th>Color</th>
                <th>Text</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            {% for highlight in highlights %}
            <tr>
                <td>{{ highlight.ID }}</td>
                <td>{{ highlight.book }}</td>
                <td>{{ highlight.chapter_number }}</td>
                <td>{{ highlight.page_number }}</td>
                <td>{{ highlight.html_line_number }}</td>
                <td>{{ highlight.color }}</td>
                <td>{{ highlight.text }}</td>
                <td>{{ highlight.timestamp }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="8" style="text-align: center;">No highlights found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
{% endblock %}


this is my views.py file:

# timwise.views.py
# # cd /home/django/django_project
# source bin/activate
from django import forms
from django.shortcuts import render, redirect
from .models import Book, Author, Highlight, Files
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy #from gemini
from .forms import FileUploadForm #from gemini
from django.contrib import messages #from gemini
from bs4 import BeautifulSoup, SoupStrainer
# import html5lib
from django.contrib.auth.mixins import LoginRequiredMixin
import logging, os, re
from timeout_decorator import timeout
from django.contrib.auth.models import User
from datetime import datetime
import datetime as dt
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView



class Author_list(ListView):
    model = Highlight
    template_name = "highlights_list.html"

class Book_list(ListView):
    model = Highlight
    template_name = "highlights_list.html"

class Highlight_list(ListView):
    model = Highlight
    template_name = "highlights_list.html"

class UploadHighlights(CreateView):
    model = Highlight
    template_name = "upload_highlights.html"
    fields = ["chapter_number", "html_line_number", "color", "page_number","text"]

class EditAuthorView(UpdateView):
    model = Author
    template_name = "edit_author.html"
    fields = ["lastname", "firstname", "fullname"]  # Fields to edit
    success_url = reverse_lazy("myauthors")  # Redirect after successful edit

    def get_object(self, queryset=None):
        author_id = self.kwargs.get("id")
        return Author.objects.get(ID=author_id)

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "yearwritten"]
        widgets = {
            "name": forms.Textarea(attrs={
            "class": "custom-textarea",
            "wrap": "soft",
         }),
}

class EditBookView(UpdateView):
    model = Book
    template_name = "edit_book.html"
    form_class = EditBookForm
    # fields = ["name", "yearwritten"]  # Fields to edit
    success_url = reverse_lazy("mybooks")  # Redirect after successful edit

    def get_object(self, queryset=None):
        book_id = self.kwargs.get("id")
        return Book.objects.get(ID=book_id)

########################### edit highlight classes ########################################




########################### edit highlight classes ########################################

class FileUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FileUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('success')

    def dispatch(self, request, *args, **kwargs):
        print(f"DEBUG: Request method: {request.method}")
        print(f"DEBUG: Request headers: {dict(request.headers)}")
        print(f"DEBUG: Request META: {dict(request.META)}")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("DEBUG: Post request received")
        print(f"DEBUG: Post data: {dict(request.POST)}")
        print(f"DEBUG: Files: {dict(request.FILES)}")
        
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            import traceback
            print(f"ERROR in post: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise

    # @timeout(30)
    def form_valid(self, form):
        # TODO: cleanup form_valid
        highlight_upload_count=0
        highlight_NOT_upload_count=0
        msg="   1. DEBUG: Starting form_valid method."
        
        try:
            now = datetime.now()
            datewhenuploaded=str(now.strftime("%m/%d/%Y"))            
            file = form.save(commit=False)
            
            # Ensure the user is attached to the file
            file.user = self.request.user
            file.save()
            
            # Rest of your processing...
            user_id = self.request.user.id
            user_name = self.request.user.username
            session_id = self.request.session.session_key
            filename = file.file.name 
            msg=msg + "  2.  Filename is: " + filename

            with file.file.open() as hdoc:
                strainer = SoupStrainer('div')
                content = hdoc.read()                
                soup = BeautifulSoup(content, 'html.parser')

            book_title=soup.find(class_ = "bookTitle")
            book_name=book_title.text.strip()
            msg=msg + "  3.  The book name is: " + book_name

            citation_string=soup.find(class_ = "citation")

            ctext=citation_string.text.strip()

            try:
                year_match = re.search(r'\d{4}', ctext)
                year = int(year_match.group())

            except:
                year = 9999

            msg=msg + f"  4.    The year is: {year}"

            author=soup.find(class_ = "authors")
            author_name = author.text.strip()
            author_name=author_name.rstrip('\n')
            author_name=author_name.lstrip('\n')

            author_last_name=author_name.split(',')[0]
            author_first_name=author_name.split(', ')[1]

            try:

                user_obj = User.objects.filter(id=user_id).first()

                author_obj, created = Author.objects.get_or_create(
                    fullname=f"{author_first_name} {author_last_name}",
                    user=user_obj,
                    defaults={
                        'firstname': author_first_name,
                        'lastname': author_last_name,
                        'dateloaded':datewhenuploaded,
                        'sessionkey':session_id,                }
                    )

            except Exception as e:
                msg=msg+f"Failed to create author, the resulting error message is: {e}"


            authorid=author_obj.ID 

            divs = soup.findAll('div', class_='sectionHeading')
            chapter_quantity=len(divs)

            msg=msg + "  5.  The author is: " + author_name + ", the authorID is:" +str(authorid)+ ", The chapter count is: " + str(chapter_quantity)

            msg=msg+"  6.  .......CHECKING IF BOOK EXISTS...."


            book_obj = Book.objects.filter(name=book_name).first()
            msg=msg+".......CHECKED....."
 

            try:

                book_obj, created = Book.objects.get_or_create(
                    name=book_name,
                    author=author_obj,
                    user=user_obj,
                    defaults={
                        'chaptercount': chapter_quantity,
                        'yearwritten': year,
                        'dateloaded': datewhenuploaded,
                        'sessionkey': session_id,
                    }
                )

            except Exception as e:
                msg=msg+f"Failed to create book, the resulting error message is: {e}"

            msg=msg+"...... BOOK ENTRY CREATED....."
             
            msg=msg+"  8.  .......BOOK DATABASE UPDATE PROCEDURE PASSED...."
            
            try:

                book_id=book_obj.ID

            except Exception as e:
                msg=msg+f'failed to get book id book, the resulting error message is: {e}'
                
            msg=msg+f"   9.  GOT BOOK ID  {book_id}........ "


            notes = soup.findAll('div', class_='noteText')
            noteqty=len(notes)  
            msg=msg+f"  11.  NOTES AGGREGATED....THERE ARE {noteqty} NOTES....."

            higlight_array=[]
            z=1
            for note in notes:

                text=note.text
                text=text.strip()
                notelinenumber= note.sourceline
                higlight_array.append(text)                 
                if z==1:
                    msg=msg+f"the first note is: {text} and line number of note is: {notelinenumber}"

                target_sourceline=note.sourceline-3
                notesheading = soup.findAll('div', class_='noteHeading')
                for head in notesheading:
                    if head.sourceline==target_sourceline:
                        page_info=head.text
                        head, sep, tail = page_info.partition('Page ')
                        page_number=tail.strip()
                        start = '('
                        end = ')'
                        s = page_info
                        highlight_color=(s.split(start))[1].split(end)[0]



                    if z==1:
                        msg=msg+".......CHECKING IF HIGHLIGHT NOTE EXISTS....."
                    try:

                        highlight_obj = Highlight.objects.filter(text=text).first()
                        if z==1 and highlight_obj:
                            msg=msg+".......HIGHLIGHT CHECKED, HIGHLIGHT EXISTS....."

                        if z==1 and not highlight_obj:
                            msg=msg+".......HIGHLIGHT CHECKED, HIGHLIGHT DOES NOT EXIST....."
                                                # 
                    except Exception as e:
                        if z==1:
                            msg=msg+f"Failed to READ highlight, the resulting error message is: {e}"  
                    try:


                        highlight_obj, created = Highlight.objects.get_or_create(
                            text=text,
                            defaults={
                                'chapter_number': z,
                                'html_line_number': note.sourceline,
                                'color': highlight_color,
                                'page_number': page_number,
                                'book_id':book_id,
                                'sessionkey':session_id,
                                'user':user_obj,
                                'dateloaded':datewhenuploaded
                            }
                        )                           

                        if not highlight_obj: #highlight does not exist
                            
                            highlight_upload_count=highlight_upload_count+1

                        if highlight_obj:
                            highlight_NOT_upload_count=highlight_NOT_upload_count+1



                    except Exception as errortext:
                        msg=msg+f"Failed to WRITE highlight, the resulting error message is: {errortext}"                            

                    z=z+1

            try:
                uploadstatmessage=" " 
                numberofhighlights=len(higlight_array)
                # highlight_upload_count = Highlight.objects.filter(sessionkey=session_id).count()
                numberofpreviouslyuploadedhighlights= numberofhighlights-highlight_upload_count
                # highlight_NOT_upload_count

                msg2=f"there are {numberofhighlights} highlights inside the html file, {highlight_upload_count} was(were) uploaded, and {highlight_NOT_upload_count} was(were) NOT uploaded."

                if numberofhighlights==highlight_upload_count and highlight_upload_count>1:
                    uploadstatmessage=f"All {numberofhighlights} highlights are new and all {highlight_upload_count} were uploaded"

                if numberofhighlights==highlight_upload_count and highlight_upload_count==1 and numberofhighlights>1:
                    uploadstatmessage=f"Only {numberofhighlights} of the {highlight_upload_count} highlights are new"

                if numberofhighlights==highlight_upload_count and highlight_upload_count==1 and numberofhighlights==1:
                    uploadstatmessage=f"The {numberofhighlights} highlight from the processed html file is new"

                if numberofhighlights!=highlight_upload_count:
                    uploadstatmessage=f"Of the {numberofhighlights} highlight(s) from the processed html file, { highlight_upload_count } are new"



                Authorfullname=f"{author_first_name} {author_last_name}"
                context = {
                            'book': book_name,
                            'author': Authorfullname,
                            'user':user_obj,
                            'highlights': higlight_array,
                            'numberofhighlights':numberofhighlights,
                            'highlight_upload_count':highlight_upload_count,
                            'uploadstatmessage':uploadstatmessage,
                            'msg2':msg2,
                        }

                return render(self.request, 'upload_success.html', context)

            except Exception as errortext:
                msg=msg+f"Failed to Render html page, the resulting error message is: {errortext}"   
                return self.form_invalid(form, msg)                    



        except Exception as e:
            import traceback
            return self.form_invalid(form, msg)

    def form_invalid(self, form, msg):
        messages.error(self.request, f"Processing the File upload failed. Please check the file and try again. {msg} ")
        return super().form_invalid(form)

def home(request):
    return render(request, 'home.html')

def why(request):
    return render(request, 'why.html')

def instructions(request):
    return render(request, 'instructions.html')

def profile(request):
    return render(request, 'profile.html')

def myhighlights(request):
    
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': 'You need to log in to view your highlights.'})

    user_id = request.user.id
    user_name = request.user.username
    session_id = request.session.session_key

    # Filter highlights for the logged-in user
    highlights = Highlight.objects.filter(user_id=user_id)

    # Pass context to the template
    context = {
        'user_id': user_id,
        'user_name': user_name,
        'session_id': session_id,
        'highlights': highlights,
    }

    return render(request, 'myhighlights.html', context)

def settings(request):
    return render(request, 'settings.html')

def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')

def signup(request):
    return render(request, 'signup.html')

def myauthors(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': 'You need to log in to view your highlights.'})

    user_id = request.user.id
    user_name = request.user.username
    session_id = request.session.session_key
    
    # Filter highlights for the logged-in user
    authors = Author.objects.filter(user_id=user_id)
    qty_of_authors = len(authors)

    context = {
        'user_id': user_id,
        'user_name': user_name,
        'session_id': session_id,
        'authors': authors,
        'qty_of_authors': qty_of_authors,
    }


    return render(request, 'myauthors.html', context)



def mybooks(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': 'You need to log in to view your highlights.'})

    user_id = request.user.id
    user_name = request.user.username
    session_id = request.session.session_key
    
    # Filter highlights for the logged-in user
    books = Book.objects.filter(user_id=user_id)
    qty_of_books = len(books)

    context = {
        'user_id': user_id,
        'user_name': user_name,
        'session_id': session_id,
        'books': books,
        'qty_of_books': qty_of_books,
    }


    return render(request, 'mybooks.html', context)

this is my models.py file:

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
    
    this is my urls.py file:

# timwise django app
# timwise.urls.py


from django.urls import path, include
# TODO: test commenting out the next line
from .views import UploadHighlights, FileUploadView, EditAuthorView, EditBookView
from django.views.generic import TemplateView
from django.http import HttpResponse
import logging
from django.conf import settings 
from . import views  # new from AI, Import the views module from the current app

logger = logging.getLogger(__name__)

def test_logging(request):
    print("PRINT: Test view executed")
    logger.debug("DEBUG: Test view executed")
    logger.info("INFO: Test view executed")
    logger.warning("WARNING: Test view executed")
    logger.error("ERROR: Test view executed")
    return HttpResponse("Test view executed - check your console")

urlpatterns = [
    path('', views.home, name='home'),
    path('test-logging/', test_logging, name='test-logging'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('success/<str:filename>/<str:msg>/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('home/', views.home, name='home'),
    path('edit-author/<int:id>/', EditAuthorView.as_view(), name='edit-author'),
    path('edit-book/<int:id>/', EditBookView.as_view(), name='edit-book'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('myauthors/', views.myauthors, name='myauthors'),
    path('why/', views.why, name='why'),
    path('settings/', views.settings, name='settings'),
    path('myhighlights/', views.myhighlights, name='myhighlights'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('instructions/', views.instructions, name='instructions'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


