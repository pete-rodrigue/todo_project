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
            # we'll put code here telling the user their passwords
            # didn't match!
            print("passwords didn't match!")
