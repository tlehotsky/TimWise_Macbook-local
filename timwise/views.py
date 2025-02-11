# timwise.views.py


# source bin/activate
from django.shortcuts import get_object_or_404
from django import forms
from django.shortcuts import render, redirect
from .models import Book, Author, Highlight, Files, UserSettings
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy #from gemini
from .forms import FileUploadForm #from gemini
from django.contrib import messages #from gemini
from bs4 import BeautifulSoup, SoupStrainer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging, os, re
from timeout_decorator import timeout
from django.contrib.auth.models import User
from datetime import datetime
import datetime as dt
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import UpdateView


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "edit_profile.html"
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy("edit_profile")  # Redirect to the same page or elsewhere after saving

    def get_object(self, queryset=None):
        # Return the current logged-in user
        return self.request.user

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


class EditUserSettingsView(LoginRequiredMixin, UpdateView):
    model = UserSettings
    template_name = "settings.html"
    fields = ["theme", "font_size", "font_family", "line_height", "margin", "emailfrequency", "qtyperemail", "repeatsendhightlights"]
    success_url = reverse_lazy("settings")  # Redirect to the same page or elsewhere after saving

    def get_object(self, queryset=None):
        # Get or create the UserSettings object for the logged-in user with default values
        obj, created = UserSettings.objects.get_or_create(
            user=self.request.user,
            defaults={
                "theme": "default",
                "font_size": 8,
                "font_family": "Arial",
                "line_height": 1.5,
                "margin": 10,
                "emailfrequency": "daily",
                "repeatsendhightlights": False,
                "qtyperemail": 1,
            }
        )
        return obj



########################### edit highlight classes ########################################

class EditHighlightView(UpdateView):
    model = Highlight
    template_name = "edit_highlight.html"
    fields = ["name", "html_line_number", "color", "page_number", "text"]  # Fields to edit
    success_url = reverse_lazy("myhighlights")  # Redirect after successful edit


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

                        highlight_obj = Highlight.objects.filter(text=text, user=user_obj).first()
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
                            user=user_obj,
                            defaults={
                                'chapter_number': z,
                                'html_line_number': note.sourceline,
                                'color': highlight_color,
                                'page_number': page_number,
                                'book_id':book_id,
                                'sessionkey':session_id,
                                'dateloaded':datewhenuploaded
                            }
                        )

                    # highlight_obj = Highlight.objects.create(
                    #         text=text,
                    #         user=user_obj,
                    #         chapter_number=z,
                    #         html_line_number=note.sourceline,
                    #         color=highlight_color,
                    #         page_number=page_number,
                    #         book_id=book_id,
                    #         sessionkey=session_id,
                    #         dateloaded=datewhenuploaded
                    #         )






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
                            'logreport':msg,
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

def logmeout(request):
    auth_logout(request)
    return render(request, 'logmeout.html')

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

# @require_http_methods(["GET", "POST"])  # Only allow GET and POST methods
# def custom_logout(request):
#     auth_logout(request)
#     return redirect('home')


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

# def edit_highlight(request, pk):
#     # Your view logic here
#     return render(request, 'edit_highlight.html', context={})