# admin.py - Configuration for Django Admin Interface

# This file defines how the models in this app are displayed and managed
# through the Django Admin Interface. It includes model registration,
# customization, permissions, and more for admin users.

from django.contrib import admin
from .models import ToDoList, ItemsInToDoList, Date, CustomUser

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(ItemsInToDoList)
admin.site.register(Date)
admin.site.register(CustomUser)