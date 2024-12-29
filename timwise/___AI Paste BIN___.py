for my timwise django app, please help me make the text box for the book name field wider.
    
thie is my class view:
    
class EditBookView(UpdateView):
    model = Book
    template_name = "edit_book.html"
    fields = ["name", "yearwritten"]  # Fields to edit
    success_url = reverse_lazy("mybooks")  # Redirect after successful edit

    def get_object(self, queryset=None):
        book_id = self.kwargs.get("id")
        return Book.objects.get(ID=book_id)   
    

this is my template:

{% extends "base.html" %}

{% block content %}
<h1>Edit Book</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
</form>
<a href="{% url 'mybooks' %}">Cancel</a>
{% endblock %}