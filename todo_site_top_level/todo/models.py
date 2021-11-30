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
    time_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # gotta tie the todo object to a specific user
    # so we're gonna tie this model to the user model
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


    def __str__(self):
        # this lets us see the name of the object in the admin GUI
        return self.title
