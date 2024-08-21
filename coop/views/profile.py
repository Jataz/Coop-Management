from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser

from ..forms import LoanApplicationForm

@login_required(login_url="/login")
def user_profile(request):
    context = {
        'active_page': 'user-profile'
    }
    return render(request,'pages/profile/index.html',context)

@login_required(login_url="/login")
def edit_profile(request):
    return render(request,'pages/profile/edit.html')

@login_required(login_url="/login")
def change_password(request):
    context = {
        'active_page': 'change-password'
    }
    return render(request,'pages/profile/change_password.html',context)