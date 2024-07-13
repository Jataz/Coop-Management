from django import forms
from django.contrib.auth.forms import  AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import LoanApplication 


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter phone number", "class": "form-control"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter full name", "class": "form-control"}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    id_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter ID number", "class": "form-control"}))
    sex = forms.ChoiceField(choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female')],widget=forms.Select(attrs={"class": "form-control"}))
    physical_address = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter physical address", "class": "form-control", "rows": 3}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "phone_number", "full_name", "date_of_birth", "id_number", "sex", "physical_address", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))

    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }
    

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['mobile_account', 'amount', 'term_months', 'agreed_to_terms']
        widgets = {
            'term_months': forms.NumberInput(attrs={'min': 1}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    