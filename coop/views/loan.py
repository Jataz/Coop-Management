from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import CustomUser, LoanApplication, LoanStatus

from ..forms import LoanApplicationForm


@login_required(login_url="/login")
def loan_transactions(request):
    # Filter loans that belong to the current logged-in user
    loans = LoanApplication.objects.filter(borrower=request.user)
    context = {
        'loans': loans,
        'active_page': 'loan-transactions'
    }
    return render(request, 'pages/loan/transaction.html', context)


@login_required(login_url="/login")
def loan_apply(request):
    context = {
        'active_page': 'loan-application'
    }
    return render(request, 'pages/loan/apply.html', context)

@login_required
def loan_application(request):
    user = request.user
    
    # Redirect to loan status if the user has an outstanding loan
    outstanding_loan = LoanApplication.objects.filter(borrower=user, status='Outstanding').first()
    if outstanding_loan:
        return redirect('loan-status', pk=outstanding_loan.pk)
    
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            loan_data = form.cleaned_data
            borrower = request.user

            # Check if the user already has an outstanding loan
            if LoanApplication.objects.filter(borrower=borrower, status='outstanding').exists():
                messages.error(request, "You cannot apply for a new loan while you have an outstanding loan.")
                return redirect('loan-application')
            
            # Prepare loan data for session
            loan_data['borrower'] = borrower.id  # Store borrower id for reference
            loan_data['amount'] = float(loan_data['amount'])  # Convert amount to float

            # Store the data in session for confirmation
            request.session['loan_data'] = loan_data
            
            # Redirect to confirmation page
            return redirect('loan-confirm')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoanApplicationForm()

    # Render loan application form

    context = {
        'form': form,
        'active_page': 'loan-application'
    }
    return render(request, 'pages/loan/application.html', context)

@login_required
def confirm_loan(request):
    loan_data = request.session.get('loan_data')
    
    if not loan_data:
        messages.error(request, 'Loan application data not found.')
        return redirect('loan-application')

    # Retrieve logged-in user using stored identifier
    borrower_identifier = loan_data['borrower']
    borrower = CustomUser.objects.get(id=borrower_identifier)  # Adjust this based on your User model
    
    # Convert float values to Decimal
    amount = Decimal(str(loan_data['amount']))
    term_months = loan_data['term_months']
    interest_rate = Decimal('5.00')  # Assuming a fixed interest rate
    service_fee = Decimal('10.00')

    # Calculate values for confirmation page
    interest = (amount * (interest_rate / Decimal('100')) * term_months)
    repayment_amount = amount + interest
    disbursed_amount = amount - service_fee
    due_date = datetime.now() + timedelta(days=30 * term_months)

    if request.method == 'POST':
        try:
            # Create LoanApplication object
            loan_application = LoanApplication.objects.create(
                borrower=borrower,
                mobile_account=loan_data['mobile_account'],
                amount=amount,
                term_months=term_months,
                interest_rate=interest_rate,
                service_fee=service_fee,
                repayment_amount=repayment_amount,
                due_date=due_date,
                agreed_to_terms=loan_data['agreed_to_terms'],
                disbursed_amount=disbursed_amount ,
                status='Outstanding'
            )

            # Create LoanStatus object
            LoanStatus.objects.create(
                loan_application=loan_application,
                outstanding_amount=repayment_amount,
                due_date=due_date,
                total_to_be_repaid=repayment_amount,
                summary_interest=interest,
                overdue_mgt_fee=Decimal('0'),
                late_interest=Decimal('0'),
                partial_payment=Decimal('0'),
            )

            # Clear session data after successful submission
            del request.session['loan_data']

            # Redirect to loan status page with loan_application.pk
            return redirect('loan-transactions')
        
        except Exception as e:
            messages.error(request, f'Failed to process loan application: {str(e)}')
            return redirect('loan-application')

    context = {
        'borrower': borrower,
        'amount': amount,
        'term_months': term_months,
        'service_fee': service_fee,
        'interest': interest,
        'repayment_amount': repayment_amount,
        'disbursed_amount': disbursed_amount,
    }
    
    return render(request, 'pages/loan/confirm_loan.html', context)


@login_required
def loan_payment(request):
    try:
        # Filter loan applications with 'outstanding' status
        loan_application = LoanApplication.objects.filter(status='Outstanding').first()
        
        if not loan_application:
            messages.error(request, "No outstanding loan applications found.")
            return redirect('loan-transactions')  # Redirect to a list of loans or appropriate page

        loan_status = get_object_or_404(LoanStatus, loan_application=loan_application)
        
        if request.method == 'POST':
            repayment_amount = Decimal(request.POST.get('repayment_amount'))
            
            # Calculate the remaining amount
            loan_status.partial_payment += repayment_amount
            loan_status.outstanding_amount -= repayment_amount
            
            # If the outstanding amount is zero or less, mark the loan as cleared
            if loan_status.outstanding_amount <= 0:
                loan_application.status = 'Cleared'
                loan_status.outstanding_amount = 0  # Ensure it doesn't go negative
            
            loan_status.save()
            loan_application.save()

            messages.success(request, "Loan repayment successful.")
            return redirect('loan-status', pk=loan_application.pk)

        context = {
            'loan_application': loan_application,
            'loan_status': loan_status,
            'outstanding_amount': loan_status.outstanding_amount,
        }
        return render(request, 'pages/loan/repayment.html', context)

    except LoanApplication.DoesNotExist:
        messages.error(request, "No outstanding loan applications found.")
        return redirect('loan-transactions')  # Redirect to a list of loans or appropriate page

@login_required
def repay_loan(request, pk):
    loan_application = get_object_or_404(LoanApplication, pk=pk)
    loan_status = get_object_or_404(LoanStatus, loan_application=loan_application)

    if loan_application.status != 'Outstanding':
        messages.error(request, "Repayments can only be made to loans with an outstanding status.")
        return redirect('loan-status', pk=loan_application.pk)

    if request.method == 'POST':
        repayment_amount = Decimal(request.POST.get('repayment_amount'))
        
        # Calculate the remaining amount
        loan_status.partial_payment += repayment_amount
        loan_status.outstanding_amount -= repayment_amount
        
        # If the outstanding amount is zero or less, mark the loan as cleared
        if loan_status.outstanding_amount <= 0:
            loan_application.status = 'Cleared'
            loan_status.outstanding_amount = 0  # Ensure it doesn't go negative
        
        loan_status.save()
        loan_application.save()

        messages.success(request, "Loan repayment successful.")
        return redirect('loan-transactions', pk=loan_application.pk)

    context = {
        'loan_application': loan_application,
        'loan_status': loan_status,
        'outstanding_amount': loan_status.outstanding_amount,  # Pass outstanding amount
    }
    return render(request, 'pages/loan/repayment.html', context)

def loan_status(request, pk):
    loan_application = get_object_or_404(LoanApplication, pk=pk)
    loan_status = loan_application.Loan_application_status
    loan_stats = loan_application.status

    if loan_stats == 'Outstanding':
        template_name = 'pages/loan/loan_outstanding.html'
    else:
        template_name = 'pages/loan/loan_status.html'

    context = {
        'loan': loan_application,
        'loan_status': loan_status
    }

    return render(request, template_name, context)

def loan_outstanding(request, pk):
    loan_application = LoanApplication.objects.get(pk=pk)
    loan_status = loan_application.Loan_application_status
    context ={
        'loan':loan_application,
        'loan_status':loan_status
    }
    return render(request, 'pages/loan/loan_outstanding.html', context)

