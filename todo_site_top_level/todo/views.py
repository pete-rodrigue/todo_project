from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm          # this is our form
from .models import todo_list_item   # this is our todo list database
from django.utils import timezone



# Create your views here.

def home(request):
    # the home page
    return render(request, template_name='home_template.html')



def signupuser(request):
    '''
    note that we don't have to create a new "user"
    model or database in our project, because
    Django comes pre-loaded with a user database!
    '''
    if request.method == 'GET':
        # if the request is "get" just show the webpage
        return render(request,
            template_name='signupuser_template.html',
            context = {'form':UserCreationForm()})
    else:
        # if the method is "post", create and save a new user!
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_user = User.objects.create_user(
                                 username=request.POST['username'],
                                 password=request.POST['password1'])
                new_user.save()
                login(request, new_user)

                return redirect(to='current_todos')

            except IntegrityError:
                return render(request,
                    template_name='signupuser_template.html',
                    context = {'form':UserCreationForm(),
                               'some_kind_of_error':'Already a user with that name, please choose a new username!'})
        else:
            # if the 2 passwords don't match, basically serve the user
            # the same page again,
            return render(request,
                template_name='signupuser_template.html',
                context = {'form':UserCreationForm(),
                           'some_kind_of_error':'Passwords did not match!'})



def logoutuser(request):
    # logs out the user
    if request.method == "POST":
        logout(request)

        return redirect('home')


def loginuser(request):
    # logs in an existing user
    if request.method == 'GET':
        # if the request is "get" just show the login page
        return render(request,
            template_name='login_template.html',
            context = {'form':AuthenticationForm()})
    else:
        # if there's a POST, try to authenticate the user
        existing_user = authenticate(request,
                                     username=request.POST['username'],
                                     password=request.POST['password'])
        if existing_user is None:
            # if there's an error, show the log in page w/ an error message
            return render(request,
                template_name='login_template.html',
                context = {'form':AuthenticationForm(),
                           'some_kind_of_error':'Username and password did not match'})
        else:  # if we can authenticate the user...
            # log them in and send them to the current todos page
            login(request, existing_user)
            return redirect(to='current_todos')


def current_todos(request):
    # the page with the current todo items
    my_todos = todo_list_item.objects.filter(user=request.user,  # ensures users only see their todos
                                             time_completed__isnull=True)  # ensures completed tasks do not appear

    return render(request,
                  template_name='current_todos_template.html',
                  context={'todos_context': my_todos})


def create_todo(request):
    # allows a user to create a new todo
    if request.method == "GET":
        return render(request,
            template_name='create_todo_template.html',
            context = {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)  # don't commit to database yet
            new_todo.user = request.user        # add user, then save
            new_todo.save()
        except ValueError:
            render(request,
                template_name='create_todo_template.html',
                context = {'form':TodoForm(),
                           'some_kind_of_error':"You've entered some bad data!"})

        return redirect(to='current_todos')   # send the user to the current
                                              # todos webpage.


def view_todo(request, todo_pk):
    # allows a user to view a single todo item
    single_todo = get_object_or_404(todo_list_item,
                                    pk=todo_pk,
                                    user=request.user)  # ensures users can only open their own todos
    if request.method == 'GET':
        form = TodoForm(instance=single_todo)
        return render(request,
                      template_name='view_todo_template.html',
                      context={'single_todo_context':single_todo,
                               'prefilled_form':form})
    else:
        try:
            revised_form = TodoForm(request.POST, instance=single_todo)
            revised_form.save()
            return redirect(to='current_todos')   # send the user to the current
                                                  # todos webpage.
        except ValueError:
            return render(request,
                          template_name='view_todo_template.html',
                          context={'single_todo_context':single_todo,
                                   'prefilled_form':form,
                                   'some_kind_of_error':"You've entered some bad data!"})


def complete_todo(request, todo_pk):
    todo = get_object_or_404(todo_list_item, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.time_completed = timezone.now()
        todo.save()
        return redirect('current_todos')       # send the user to the current
                                              # todos webpage.


def delete_todo(request, todo_pk):
    todo = get_object_or_404(todo_list_item, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')       # send the user to the current
                                              # todos webpage.
