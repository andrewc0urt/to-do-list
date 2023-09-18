from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Custom fields here
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)

    # Exclude the username field
    username = None

    # Use the email field as the username field for authentication
    USERNAME_FIELD = 'email'

    # Include first_name and last_name in REQUIRED_FIELDS
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# retrieves the user model (CustomUser) defined in Django project's settings in AUTH_USER_MODEL 
User = get_user_model()

class ToDoList(models.Model):  # Actual Entire To-Do List
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"To-Do List for {self.user.username}"
    
class ItemsInToDoList(models.Model):  # Individual Items in the To-Do List
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.item + '    |   ' + str(self.completed)

class Date(models.Model):
    current_date = models.DateField()