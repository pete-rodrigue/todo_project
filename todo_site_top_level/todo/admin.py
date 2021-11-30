from django.contrib import admin
from .models import todo_list_item


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created',)

# Register your models here.
admin.site.register(todo_list_item, TodoAdmin)
