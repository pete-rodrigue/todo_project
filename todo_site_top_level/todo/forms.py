
from django.forms import ModelForm
from .models import todo_list_item



# makes the form that allows us to add todo items
class TodoForm(ModelForm):
    class Meta:
        model = todo_list_item  # the model, taken from models.py
        fields = ['title', 'description', 'important']
