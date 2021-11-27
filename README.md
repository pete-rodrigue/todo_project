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

Now wrap that form bit in a form tag, and add a submit button, so our users can submit their sign up info, like this:

```
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>
```

The `{% csrf_token %}` bit is required by Django. It helps prevent a type of attack called a Cross Site Request Forgery (more on that here: https://www.youtube.com/watch?v=vRBihr41JTo). Note that a "post" doesn't put any text into the URL bar--we wouldn't want people's passwords in the URL bar!

