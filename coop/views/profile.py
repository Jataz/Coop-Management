from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser

from ..forms import LoanApplicationForm, UserProfileForm

@login_required(login_url="/login")
def user_profile(request):
    user = request.user  # Get the logged-in user
    context = {
        'active_page': 'user-profile',
        'user': user  # Pass the user object to the context
    }
    return render(request,'pages/profile/index.html',context)


@login_required(login_url="/login")
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')  # Redirect to the profile page or another page
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'active_page': 'edit-profile',
        'form': form
    }
    return render(request, 'pages/profile/edit.html', context)

@login_required(login_url="/login")
def change_password(request):
    context = {
        'active_page': 'change-password'
    }
    return render(request,'pages/profile/change_password.html',context)