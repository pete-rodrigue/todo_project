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
