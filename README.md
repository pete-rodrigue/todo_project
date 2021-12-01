## Walkthrough

This code creates a simple django website that allows users to create accounts and save personal todo lists.
At some point I may revise this to mimic the tracking project I'm working on at EPA. Or I may make that in a different repo.
Anyway this whole thing is based on a Udemy course called _Django 3 - Full Stack Websites with Python_ by Nick Walter: https://www.udemy.com/course/django-3-make-websites-with-python-tutorial-beginner-learn-bootstrap/

Here is what I did.

### Basic Setup

I used anaconda for this project. ¯\\_(ツ)_/¯

On my laptop, in `OneDrive/Documents/GitHub`, create a folder called todo_project. 

Open the anaconda command prompt. 

cd into `OneDrive/Documents/GitHub/todo_project`

execute: `django-admin startproject todo_site` 

This creates our django project, called todo_site. I renamed this folder "todo_site_top_level". So the folder structure is:

todo_project<br>
|<br>
|__ todo_site_top_level<br>
&nbsp;    |<br>
&nbsp;    |__ manage.py<br>
&nbsp;    |__ todo_site<br>

Then execute:
`pip install python-dotenv`

This is a module that will allow us to keep our secret django key hidden in a file called `.env` We will store this `.env` file locally on our computer, 
and keep it from being uploaded to GitHub by including this `.env` file in our `.gitignore` file.

So we need to create a file called `.gitignore` that contains the text `.env`. This file should live in our root folder. The `.env` file should also live in our root folder, and should contain your secret key, like this: `SECRET_KEY=<YOUR SECRET KEY GOES HERE>`. So the file structure now looks like:

todo_project<br>
|<br>
|__ todo_site_top_level<br>
&nbsp;    |<br>
&nbsp;    |__ manage.py<br>
&nbsp;    |__ .env<br>
&nbsp;    |__ .gitignore<br>
&nbsp;    |__ todo_site<br>


Then you'll want to add the following to the top of settings.py in the todo_site folder: 

`import os`

`from dotenv import load_dotenv`

`load_dotenv()`

And you'll want to add this line in place of the old secret key assignment: `SECRET_KEY = str(os.getenv('SECRET_KEY'))`

That's it! Now you're secret key won't be posted to the internet. Just make sure to change the key from the default value. If you haven't already, now might be a good time to connect this project to a git repo.

### Making our first app on this new site

Create our first django app for this new site by navigating to `todo_site_top_level` and executing `python manage.py startapp todo` in the command line. Now go to `settings.py` in `todo_site` and add `todo` to the list of installed apps. At this point, you should be able to execute `python manage.py runserver`, go to localhost:8000 in your browser, and see your "website": the django default webpage (there should be a message that says something like "The install worked successfully! Congratulations!"). 

Hit ctrl+c in the command line to stop running the "server." Then execute `python manage.py migrate` to migrate the initial apps.

### Building the sign up feature

We need to create a user signup page, and tell the website about this signup page. Go to `urls.py` in `todo_site` and add this import:

`from todo import views`

Views in django are the functions that actually render our HTML templates for the user. Each app has its own set of views. We'll get to the `views.py` file in the todo app ina minute. Add this line to the urlpatterns list in `settings.py`:

`path('signup/', views.signupuser, name='signupuser'),`

This just tells django that we're going to have a url path called something like "home/signup" and it's going to involve a view function called signupuser, which we'll need to write. So in the `todo` folder, let's add this function to `views.py`:

```
def signupuser(request):
    return render(request, template_name='signupuser_template.html')
```

Then we need to create that `signupuser_template.html` file in the `templates` folder of the `todo` folder. For now, we can just stick some placeholder text in that HTML file, like `<h1>Hello! Sign up soon!</h1>`. If you run local server again and go to _localhost:8000/signup_ you should see that text now.

Now we're going to pass forward a Django form in `views.py`, rather than creating a form from scratch. Put this at the top of `views.py`:

`from django.contrib.auth.forms import UserCreationForm`

Then revise the view we just made like this:

```
def signupuser(request):
    return render(request,
            template_name='signupuser_template.html',
            context = {'form':UserCreationForm()})
```

and go back to our `signupuser_template.html` template and add this:

`{{ form.as_p }}`

If you refresh the signup page now, you should see some basic sign in content. The "as_p" method just formats the text a little by wrapping it in `<p>` tags. You don't have to have that bit.

At this point, your sign up page should look something like this:

<img width="445" alt="bare bones sign up page" src="https://user-images.githubusercontent.com/8962291/143718477-6a82cd58-c78b-4b26-99ca-2fa302cd74c3.png">

Now wrap that form bit in a form tag, and add a submit button, so our users can submit their sign up info, like this:

```
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>
```

The `{% csrf_token %}` bit is required by Django. It helps prevent a type of attack called a Cross Site Request Forgery (more on that here: https://www.youtube.com/watch?v=vRBihr41JTo). Note that a "post" doesn't put any text into the URL bar--we wouldn't want people's passwords in the URL bar!

Ok! Let's revise the `signupuser` view to create a new user in our backend database. Make these changes:

```
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
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
            new_user = User.objects.create_user(
                                 username=request.POST['username'],
                                 password=request.POST['password1'])
            new_user.save()
        else:
            # if the 2 passwords don't match, basically serve the user
            # the same page again,
            return render(request,
                template_name='signupuser_template.html',
                context = {'form':UserCreationForm(),
                           'some_kind_of_error':'Passwords did not match!'})

```

Then go back to the html template and add this error message bit:

```
<h1>Sign up</h1>

<h2>{{some_kind_of_error}}</h2>

<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>

```

Now let's close the server and create a superuser so we can log into the admin page and see the backend database. In the command line, execute `python manage.py createsuperuser`, then create a user name and password. Re-run the server and go to _localhost:8000/admin_ to log in. If you log in and look at the Users admin page, you should see the super user you just created.

Now in another tab, go to _localhost:8000/signup_ and create a new user. First, try entering 2 different passwords; you should get that error message. Then try creating a user with identical passwords. You'll still get an error page, but if you go back to the admin page, you'll see the user you just created.

Now try creating another user with the same user name. You should get an error page, showing an "IntegrityError", because you can't create two users with the same user name. This error gets triggered when we try to execute that `user.save()` line in `views.py`. So let's go in an put a `try: except:` statement around that bit, like this:

```
if request.POST['password1'] == request.POST['password2']:
            try:
                new_user = User.objects.create_user(
                                 username=request.POST['username'],
                                 password=request.POST['password1'])
                new_user.save()
            except IntegrityError:
                return render(request,
                    template_name='signupuser_template.html',
                    context = {'form':UserCreationForm(),
                               'some_kind_of_error':'Already a user with that name, please choose a new username!'})
```

You'll also need to import the relevant module in `views.py`: `from django.db import IntegrityError`

Now if you go back and try to create another user with that same name, you should get the same page, but with an error message.

<img width="465" alt="an error msg on the signup page" src="https://user-images.githubusercontent.com/8962291/143784393-949da6db-021a-43e5-a775-654b296069a6.png">


### Logging in 

Ok. After someone signs up, we want them to be directed to the website and logged in, not just forwarded to an error page. Add this to the top of `views.py`:

`from django.contrib.auth import login`

And also, import `redirect` from `django.shortcuts`. Then add this after `user.save()`

```
login(request, new_user)
return redirect(to='current_todos')
```

add this new view:

```
def current_todos(request):
    # the page with the current todo items
    return render(request, template_name='current_todos_template.html')
```

create a new template called `current_todos_template.html` with some placeholder text in it (like "todos to come").

and add this in the `urlpatterns` list in `urls.py`:

`path('current_todos/', views.current_todos, name='current_todos'),`

Now go back to the sign in page and create a new user. You should be able to create a new user and see that landing page with the placeholder text.


### Showing the user that they're logged in

Add a new template called `base_template.html` in our `templates` folder. The template should look like this:

```
{% if user.is_authenticated %}

Logged in as {{ user.username }}

<a href="#">Logout</a>

{% else %}

<a href="#">Signup</a>
<a href="#">Login</a>

{% endif %}

{% block my_content %}
{% endblock %}
```

Then go back to our `current_todos_template.html` and replace the placeholder text with this:

```
{% extends 'base_template.html' %}

{% block my_content %}

{% endblock %}
```

Let's also add that little bit to the top of our sign in page, so people can see that login option; just remember that the `{% endblock %}` has to go after the code we already had in there, because the "my_content" block wraps around the html stuff. Note that clicking those signup/login buttons won't do anything right now, because the href directs to `#`.

### Logging users out

First, let's add a new path to `url.py` for the logout page, and (finally) one for the home page:

```
path('logout/', views.logoutuser, name='logoutuser'),
path('', views.home, name='home'),
```

Then let's tweak that href bit in our base template to remove this: `<a href="#">Logout</a>` and replace it with this:

```
<form action="{% url 'logoutuser' %}" method="post">
  {% csrf_token %}
  <button type="submit">Logout</button>
</form>
```

Then, in `views.py`, add this new view and a view for the home page:

```
def logoutuser(request):
    # logs out the user
    if request.method == "POST":
        logout(request)

        return redirect('home')
        
   
def home(request):
    # the home page
    return render(request, template_name='home_template.html')
```

Then we'll create the template for the home page.

```
{% extends 'base_template.html' %}

{% block my_content %}

<h1>Home page</h1>

{% endblock %}
```
 
Now if you go back to your website and click _Logout_, you should be logged out and sent to the homepage.

### Logging in existing users

Start by creating a new url path in `urls.py`:

```
path('login/', views.loginuser, name='loginuser'),
```

Then import `AuthenticationForm` from `django.contrib.auth.forms` and `authenticate` from `django.contrib.auth` in `views.py`.
Then add the relevant view in `views.py`:

```
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
```

And add a login html template (very similar to our sign up template):

```
{% extends 'base_template.html' %}

{% block my_content %}

<h1>Login</h1>

<h2>{{some_kind_of_error}}</h2>

<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>

{% endblock %}
```

Let's also make the _signup_ and _login_ links do something in our base template. In that template, replace the # sign in the href with the urls, like this:

```
<a href="{% url 'signupuser' %}">Signup</a>
<a href="{% url 'loginuser' %}">Login</a>
```

Ok! You should be able to log into your website now using an account you've already created.

Just to recap here, the flow looks like:

reference to url --> urls.py --> reference to a view --> views.py --> view does something


### database time!

Now we're going to make our todo model/database, to store our todo list items.

In `models.py` let's add a todo data model:

```
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class todo_list_item(models.Model):
    '''
    This is a single item in our todo list.
    '''

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_completed = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    # gotta tie the todo object to a specific user
    # so we're gonna tie this model to the user model
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
```

Then execute `python manage.py makemigrations` and `python manage.py migrate`. Then add this to `admin.py`:

```
from django.contrib import admin
from .models import todo_list_item


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created',)

# Register your models here.
admin.site.register(todo_list_item, TodoAdmin)
```

You should be able to log into the admin site and manually add todos now. To allow users to create their own todos we start in `urls.py`; add this path:

`path('create/', views.create_todo, name='create_todo'),`

Then add this view:

```
from .forms import TodoForm

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
                           'some_kind_of_error':"You've entered some bad data!""})

        return redirect(to='current_todos')   # send the user to the current
                                              # todos webpage.
```

We will update that `else` bit later. Now add the template:

```
{% extends 'base_template.html' %}
{% block my_content %}
<h1>Create</h1>
<h2>{{ error }}</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Create</button>
</form>
{% endblock %}
```

Now add a file called `forms.py` in the main folder (the one with `admin.py` and `models.py`) and put this in it:

```
from django.forms import ModelForm
from .models import todo_list_item

# makes the form that allows us to add todo items
class TodoForm(ModelForm):
    class Meta:
        model = todo_list_item
        fields = ['title', 'description', 'important']
```

What if we want to show the user their current list of todos? We'll do this next.

First, let's import our `todo_list_item` model into `views.py`: `from .models import todo_list_item`. Then let's modify our `current_todos` view, like this:

```
def current_todos(request):
    # the page with the current todo items
    my_todos = todo_list_item.objects.filter(user=request.user,  # ensures users only see their todos
                                             time_completed__isnull=True)  # ensures completed tasks do not appear

    return render(request,
                  template_name='current_todos_template.html',
                  context={'todos_context': my_todos})
```

And update `current_todos_template.html` like this:

```
{% extends 'base_template.html' %}

{% block my_content %}

<h1>Here are you todo list items:</h1>

<ul>
  {% for todo_item in todos_context %}
  <li>
    {% if todo_item.important %}<b>{% endif %}
    {{ todo_item.title }}
    {% if todo_item.important %}</b>{% endif %}
    {% if todo_item.description %}<p>{{todo_item.description}}</p>{% endif %}
  </li>
  {% endfor %}
</ul>

{% endblock %}
```

### Allowing the user to update their todo list

Let's start by updating `urls.py`:

```
path('todo/<int:todo_pk>', views.view_todo, name='view_todo'),
```

Then we'll add this bit to the top of `views.py`: `from django.shortcuts import render, redirect, get_object_or_404`


And we'll add this function to `views.py`:

```
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
```

And we'll add this new template: `view_todo_template.html`, which will look like this:

```
{% extends 'base_template.html' %}

{% block my_content %}

{{ some_kind_of_error }}

{{ single_todo_context.title }}

<form method="POST">
  {% csrf_token %}
  {{ prefilled_form.as_p }}
  <button type="submit">Save</button>
</form>
{% endblock %}
```


### Completing and deleting todos

You know the drill now!

New paths in `urls.py`: 

```
path('todo/<int:todo_pk>/complete', views.complete_todo, name='complete_todo'),
path('todo/<int:todo_pk>/delete', views.delete_todo, name='delete_todo'),
```


New view:

```
from django.utils import timezone

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
```

And add these bits to our `view_todo_template`:

```
<form method="POST" action="{% url 'complete_todo' single_todo_context.id %}">
  {% csrf_token %}
  <button type="submit">Complete</button>
</form>

<form method="POST" action="{% url 'delete_todo' single_todo_context.id %}">
  {% csrf_token %}
  <button type="submit">Delete</button>
</form>
```


### Viewing our completed todos

Add this path in `urls.py`: `path('completed/', views.completed_todos, name='completed_todos'),`

And this view:

```
def completed_todos(request):
    # the page with the current todo items
    my_todos = todo_list_item.objects.filter(user=request.user,  # ensures users only see their todos
                                             time_completed__isnull=False)  # ensures completed tasks do not appear

    return render(request,
                  template_name='current_todos_template.html',
                  context={'todos_context': my_todos})
```

And a template called `completed_todos_template.html` with this in it:

```
{% extends 'base_template.html' %}

{% block my_content %}

<h1>Here are your completed todo list items:</h1>

<ul>
  {% for todo_item in todos_context %}
  <li>
    <a href="{% url 'view_todo' todo_item.id %}">
    {% if todo_item.important %}<b>{% endif %}
    {{ todo_item.title }}
    {% if todo_item.important %}</b>{% endif %}
    </a>
    <p>{{ todo_item.time_completed }}</p>
    {% if todo_item.description %}<p>{{todo_item.description}}</p>{% endif %}
  </li>
  {% endfor %}
</ul>

{% endblock %}
```


### tidying up

Let's beef up the base template by adding some nicer styling:

```
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
```

Then revise to add these links:

```
<a href="{% url 'create_todo' %}">Create todo</a>
<a href="{% url 'current_todos' %}">Current todos</a>
<a href="{% url 'completed_todos' %}">Completed todos</a>
```

Lastly, let's ensure only logged in users can access certain pages. Go to `views.py` and add `from django.contrib.auth.decorators import login_required`. Then add this decorator on the relevant views (i.e. only views users should be able to access when logged in): `@login_required`.

Then go to `settings.py` and add this `LOGIN_URL = '/login/'`. That will forward logged out users to the login page, if they try to access a page that requires login.



That's basically it! Yay!



