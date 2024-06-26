from django.utils import timezone
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from ...forms import LoginForm, RegisterForm
from ...models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login 



def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

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

       
def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def user_logout_view(request):
  logout(request)
  return redirect('/login')