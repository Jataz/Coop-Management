from datetime import datetime, timedelta
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser, ShareCapital

from ..forms import LoanApplicationForm, ShareCapitalForm

@login_required(login_url="/login")
def share_transactions(request):
    shareCapital = ShareCapital.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'active_page': 'share-capital-transactions',
        'shareCapital': shareCapital
    }
    return render(request,'pages/shareCapital/transaction.html', context)


@login_required(login_url="/login")
def share_payment(request):
    if request.method == 'POST':
        form = ShareCapitalForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user

            # Try to fetch the first ShareCapital instance for this user
            share_capital = ShareCapital.objects.filter(user=user).first()

            # If no ShareCapital record exists, create a new one
            if not share_capital:
                share_capital = ShareCapital.objects.create(user=user, amount=0)

            try:
                share_capital.add_payment(amount)
                return JsonResponse({'status': 'success', 'message': 'Payment processed successfully.'}, status=200)
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        else:
            error_message = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'Invalid form submission.', 'errors': error_message}, status=400)

    else:
        form = ShareCapitalForm()

    return render(request, 'pages/shareCapital/payment.html', {'form': form, 'active_page': 'share-capital-payment'})
