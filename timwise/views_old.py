
####
#
#   cd /home/django/django_project

# postgreSQL token dop_v1_e24493e7dc51ea5043a81eb680ed951b10902eea794edf80b54fb40cbbc1119a

from django.shortcuts import render, redirect
from .models import Book, Author, Highlight, Files
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy #from gemini
from .forms import FileUploadForm #from gemini
from django.contrib import messages #from gemini
from bs4 import BeautifulSoup, SoupStrainer
import html5lib
from django.contrib.auth.mixins import LoginRequiredMixin
import logging, os

logger = logging.getLogger(__name__)
print("DEBUG: Views module loaded")
logger.warning("Views module loaded")

print(f"Logger name: {logger.name}")
print(f"Logger level: {logger.level}")
print(f"Logger handlers: {logger.handlers}")
print(f"Logger propagate: {logger.propagate}")

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


# class UploadFile(LoginRequiredMixin, CreateView):
#     model = Files
#     template_name = "upload_file.html"
#     fields = ["file"]

class FileUploadView(LoginRequiredMixin, CreateView): #entire class from gemini
    model = Files
    form_class = FileUploadForm
    template_name = 'upload.html'  # Create this template file
    success_url = reverse_lazy('success') # Define this url in urls.py

    def form_valid(self, form):
        file = form.save()
        user_id = self.request.user.id
        user_name=self.request.user.username
        filename = file.file.name 

        print("DEBUG: Starting form_valid method") # Basic print statement to verify output
        logger.debug("Processing file upload")
        logger.info(f"File upload started for user {user_name}")
        logger.warning(f"TEST WARNING: Processing file {filename}")
        logger.error("TEST ERROR: This should definitely show up")

        html_doc=""
        

        with file.file.open() as hdoc:
            strainer = SoupStrainer('div')
            content = hdoc.read()
            soup = BeautifulSoup(content, features="html5lib", parse_only=strainer)

            book_title=soup.find(class_ = "bookTitle")
            author=soup.find(class_ = "authors")
            author_name=(author.text)
            author_name=author_name.rstrip('\n')
            author_name=author_name.lstrip('\n')

            logger.warning("hi level warning trying to get author")


        msg = (
            f"File '{filename}' uploaded successfully! "
            f"User ID: {user_id}, Username: {user_name}. "
            f"the author is {author_name}."
        )        

        print('file loaded successfully')
        messages.success(self.request, f"File '{filename}' uploaded successfully!")
        return redirect('success', filename=filename, msg=msg) #pass the filename as a url parameter


    def form_invalid(self, form):
        # Handle form validation errors
        messages.error(self.request, "File upload failed. Please check the file and try again.")
        return super().form_invalid(form)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("DEBUG: FileUploadView initialized")
        logger.warning("FileUploadView initialized")

    def get(self, request, *args, **kwargs):
        print("DEBUG: Get request received")
        logger.warning("Get request received")
        return super().get(request, *args, **kwargs)




















