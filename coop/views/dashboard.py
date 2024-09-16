from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from ..models import LoanApplication, LoanStatus, Savings, ShareCapital, Subscription
from django.db.models import Sum


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
    
    subscription_total = Subscription.objects.aggregate(total=Sum('amount'))['total'] or 0
    share_capital_total = ShareCapital.objects.aggregate(total=Sum('amount'))['total'] or 0
    savings_total = Savings.objects.aggregate(total=Sum('amount'))['total'] or 0
    loan_total = LoanApplication.objects.filter(status='Outstanding').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'active_page': 'dashboard',
        'subscription_total': subscription_total,
        'share_capital_total': share_capital_total,
        'savings_total': savings_total,
        'loan_total': loan_total,
    }

    return render(request, 'pages/dashboard/index.html', context)