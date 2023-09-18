from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate, logout

from .forms import ListForm, SignUpForm, CustomLoginForm_CaseInsensitive
from .models import ItemsInToDoList, ToDoList, Date

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse # used to generate URLs for views
import datetime

# Create your views here.

# Function to signup - user creates an account
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:

                user = form.save(commit=False)  # create a new user instance, but don't save user to the database
                user.email = user.email.lower()  # Use 'email' instead of 'username' as noted in forms.py
                user.first_name = user.first_name.lower()
                user.last_name = user.last_name.lower()
                form.save()  # user is saved to database

                # Create a ToDoList object associated with the user - each user will only have 1 To-Do List
                ToDoList.objects.create(user=user)

            except IntegrityError: #  a user with a similar email address already exists in a case-insensitive manner (e.g., "user@example.com" and "User@example.com")
                
                # Handle the case where the email already exists in the database (case-insensitivity)
                messages.error(request, 'Account not created. Please double-check all fields. If you believe you may have already created an account using this email, please try logging in.')
                return redirect('user_signup')

            # Print the user's email to the console for debugging
            print(f"User created with email: {user.email}")
            
            # Display the success message on the signup page
            messages.success(request, "Account created! Please log in using your credentials.")

            # Redirect to the login page after successful registration instead of logging the user in automatically
            return redirect('user_login')
        
        else: 
            # Handle form errors, but only display one error alert at a time in the order in which the fields appear
            error_count = 0
            for field, error_list in form.errors.items():
                for error in error_list:
                    if "logging in" in error:
                        login_url = reverse('user_login')
                        error = error.replace("logging in", f'<a href="{login_url}">logging in</a>')
                    messages.error(request, f"{error}")
                    error_count += 1
                    break  # Break out of the inner loop after the first error

                if error_count >= 1:
                    break  # Break out of the outer loop if an error has been displayed
            
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Function to log in - user logs into their account
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm_CaseInsensitive(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')  # Use 'username' to get the email
            password = form.cleaned_data.get('password')

            # Authenticate the user using email and password
            user = authenticate(request, username=email, password=password)

            if user is not None: # if user exists in database
                django_login(request, user)

                # Redirect or perform other actions upon successful login
                return redirect('home')
            
            else:  # user not found in database (vague error message for security)
                messages.error(request, 'Invalid username or password.')
        else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = CustomLoginForm_CaseInsensitive()
    
    return render(request, 'user_login.html', {'form': form})

# Function to log out - user logs out of their account
def user_logout(request):
    logout(request)
    messages.info(request, "You've successfully logged out. Have a great day!")
    return redirect('user_login')

# Function  for the homepage - where the To-Do list lives after logging in
@login_required
def home(request):
    # Retrieve the current date
    current_date_record = Date.objects.first() # retrieve the first (and presumably only) record from the Date db model

    if current_date_record:  # if current_date_record exists (meaning it's not 'None')
        today = datetime.date.today()  # assign the current date to 'today'

        # Check if the stored date is not today's date and update if neccessary
        if current_date_record.current_date != today:
            current_date_record.current_date = today  # update the database record to reflect the current date
            current_date_record.save()
        
        # Set the curr_date to the updated current_date_record and then format it
        curr_date = current_date_record.current_date
        format_date = curr_date.strftime("%A, %B, %Y")
        curr_date = format_date
    
    else:  # if no record is found, default to datetime.date.today() to get current date and format it
        curr_date = datetime.date.today()
        format_date = curr_date.strftime("%A, %B %d, %Y")
        curr_date = format_date 

    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():

            new_item = form.save(commit=False)  # Create a new To-Do list item but don't save it yet
            new_item.todo_list = ToDoList.objects.get(user=request.user)  # Finds user's To Do List and sets the new item to the list
            new_item.save()  # Now save the new item with the associated ToDoList

            # Filter ItemsInToDoList objects by the user's ToDoList
            all_items = ItemsInToDoList.objects.filter(todo_list=new_item.todo_list)
            return render(request, 'index.html', {'all_items' : all_items, 'curr_date' : curr_date})
        
    else:
        # Get the user's ToDoList
        user_todo_list = ToDoList.objects.get(user=request.user)

        # Filter ItemsInToDoList objects by the user's ToDoList
        all_items = ItemsInToDoList.objects.filter(todo_list=user_todo_list)

        return render(request, 'index.html', {'all_items' : all_items, 'curr_date' : curr_date})
    
# Function to delete an item from the To-Do List
def delete (request, list_id):
    item = ItemsInToDoList.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ('Item Has Been Successfully Deleted!'))
    return redirect('home')  # Return to the homepage

# Function to check off an item as completed
def check_off(request, list_id):
    item = ItemsInToDoList.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')

# Function to uncheck an item from being completed
def uncheck(request, list_id):
    item = ItemsInToDoList.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')

# Function to edit an item
def edit(request, list_id):
    if request.method == 'POST':
        item = ItemsInToDoList.objects.get(pk=list_id)

        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item Has Been Updated!'))
            return redirect('home')
        
    else:
        item = ItemsInToDoList.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item' : item})
