from datetime import datetime, timedelta, timezone
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .payments.subscriptions import process_payment

from ..models import CustomUser, Subscription

from ..forms import LoanApplicationForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required(login_url="/login")
def subscriptions_transactions(request):
    
    subscriptions = Subscription.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'subscriptions':subscriptions,
        'active_page': 'subscriptions-transactions'
    }
    return render(request,'pages/subscriptions/transaction.html',context)

@login_required(login_url="/login")
def subscriptions_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Get the amount from the form data
        mobile_number = request.POST.get('mobile_number')  # Get the phone number from the form data

        if amount and mobile_number:
            try:
                amount = float(amount)  # Convert to a float if necessary

                # Prepare the data for the payment process
                payment_data = {
                    'amount': amount,
                    'mobile_number': mobile_number,
                }

                # Process the payment
                payment_result = process_payment(payment_data)

                if payment_result.get('success'):
                    start_date = datetime.now().date()
                    end_date = start_date + timedelta(days=30)   # Add 30 days to the start date

                    # Create the subscription
                    Subscription.objects.create(
                        user=request.user,
                        amount=amount,
                        start_date=start_date,
                        end_date=end_date,
                        payment_date=start_date,
                        active=True,
                    )

                    return JsonResponse({'status': 'success', 'message': "Subscription payment was successful."})
                    
                else:
                    error_message = payment_result.get('error', 'Payment failed. Please try again.')
                    return JsonResponse({'status': 'error', 'message': error_message}, status=400)

            except ValueError:
                return JsonResponse({'status': 'error', 'message': "Invalid amount entered."}, status=400)
            except Exception as e:
                logger.error(f"Unexpected error during payment processing: {str(e)}")
                return JsonResponse({'status': 'error', 'message': "An unexpected error occurred. Please try again."}, status=500)

        return JsonResponse({'status': 'error', 'message': "Please enter all required details."}, status=400)

    # Render the payment page for non-POST requests
    context = {
        'active_page': 'subscriptions-payment'
    }
    return render(request, 'pages/subscriptions/payment.html', context)