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



