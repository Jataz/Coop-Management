from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from coop.models import LoanApplication, LoanStatus, Subscription


""" @login_required(login_url="/login")
def index(request):
    subscriptions = Subscription.objects.all()
    loan_applications = LoanApplication.objects.all()
    loan_statuses = LoanStatus.objects.all()
    
    activities = list(subscriptions) + list(loan_applications) + list(loan_statuses)
    activities.sort(key=lambda x: x.updated_at, reverse=True)  # Sort by updated_at descending
    recent_activities = activities[:5]  # Get the most recent 5 activities
        context = {
        'active_page': 'dashboard'
    }

    return render(request, 'pages/dashboard/index.html', {'activities': activities}) """

@login_required(login_url="/login")
def index(request):
    
    context = {
        'active_page': 'dashboard'
    }

    return render(request, 'pages/dashboard/index.html', context)