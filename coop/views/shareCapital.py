from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser

from ..forms import LoanApplicationForm

@login_required(login_url="/login")
def share_transactions(request):
    context = {
        'active_page': 'share-capital-transactions'
    }
    return render(request,'pages/shareCapital/transaction.html')


@login_required(login_url="/login")
def share_payment(request):
    context = {
        'active_page': 'share-capital-payment'
    }
    return render(request,'pages/shareCapital/payment.html', context)