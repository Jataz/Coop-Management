from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser

from ..forms import LoanApplicationForm

@login_required(login_url="/login")
def subscriptions_transactions(request):
    return render(request,'pages/subscriptions/transaction.html')

@login_required(login_url="/login")
def subscriptions_payment(request):
    return render(request,'pages/subscriptions/payment.html')