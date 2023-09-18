from django import forms
from .models import ItemsInToDoList, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinLengthValidator # set minimum lengths for first and last name fields

class ListForm(forms.ModelForm):  # define the form
    class Meta:
        model = ItemsInToDoList
        fields = ["item", "completed"]


class SignUpForm(UserCreationForm):

    # Define validators for first_name and last_name fields
    first_name = forms.CharField(validators=[MinLengthValidator(limit_value=2, message="First name must be at least 2 characters long.")],
                                 max_length=30)
    
    last_name = forms.CharField(validators=[MinLengthValidator(limit_value=2, message="Last name must be at least 2 characters long.")],
                                 max_length=30)



    # Override the error_messages from the UserCreationForm class by passing key:value pair
    # 'password_mismatch' is the specific error code, so it goes here; the other fields are custom, so they go in Meta class
    error_messages = {
        'password_mismatch': "Passwords do not match. Please check your passwords and try again.",
    }

    class Meta:
        model=CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]

        # You can target individual fields by listing the specific field name, the key name, and the custom message
        error_messages = {
            'first_name' : {
                'required' : "Please provide a valid first name."
            },

            'last_name' : {
                'required' : "Please provide a valid last name."
            },


            'email' : {
            'unique' : "Account not created. Please double-check all fields.\nIf you believe you may have already created an account using this email, please try logging in."
            },

        }

class CustomLoginForm_CaseInsensitive(AuthenticationForm):
    # Override the clean_username function to convert email to lowercase before validating
    def clean_username(self):
        username = self.cleaned_data['username'].lower()  # Convert email to lowercase
        print(username)
        return username