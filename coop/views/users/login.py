from django.utils import timezone
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from ...forms import BeneficiaryForm, LoginForm, RegisterForm
from ...models import Beneficiary, CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password


def signupp(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Store the user data in the session instead of saving it immediately
            request.session['user_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'phone_number': form.cleaned_data['phone_number'],
                'sex': form.cleaned_data['sex'],
                'id_number': form.cleaned_data['id_number'],
                'physical_address': form.cleaned_data['physical_address'],
                'date_of_birth': str(form.cleaned_data['date_of_birth']),  # Convert to string for session storage
                'password': form.cleaned_data['password1'],  # Store the password in the session
            }
            messages.success(request, "Account details saved! Please provide beneficiary details.")
            return redirect("beneficiary-details")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def beneficiary_details(request):
    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('register')

    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            request.session['beneficiary_data'] = form.cleaned_data
            return redirect('registration-payment')
    else:
        form = BeneficiaryForm()

    context = {"form": form, "user_data": user_data}
    return render(request, "accounts/beneficiary.html", context)


def registration_payment(request):
    user_data = request.session.get('user_data')
    beneficiary_data = request.session.get('beneficiary_data')

    if not user_data or not beneficiary_data:
        return redirect('register')

    if request.method == 'POST':
        # Integrate payment gateway here
        payment_successful = True  # Replace with actual payment processing logic

        if payment_successful:
            # Create the user only after payment is successful
            user = CustomUser(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                phone_number=user_data['phone_number'],
                sex=user_data['sex'],
                id_number=user_data['id_number'],
                physical_address=user_data['physical_address'],
                date_of_birth=user_data['date_of_birth'],
                registration_fee_paid=True,
                is_member=True
            )
            user.set_password(user_data['password'])  # Hash the password before saving
            user.save()

            # Create the beneficiary associated with the user
            Beneficiary.objects.create(
                user=user,
                **beneficiary_data
            )

            # Clear session data after successful payment
            request.session.pop('user_data', None)
            request.session.pop('beneficiary_data', None)
            messages.success(request, "Payment successful and details saved! You can now log in.")
            return redirect('/login')
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('registration-payment')

    return render(request, "accounts/payment.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            return redirect("/dashboard")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("/login")
        
    return render(request, "accounts/login.html")

def user_logout_view(request):
  logout(request)
  request.session.delete()
  return redirect('/login')