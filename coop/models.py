from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import re
import uuid
from django.db import models,transaction
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
import random
import string
from django.db.models import Max
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    membership_no = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    phone_number = models.CharField(blank=True, max_length=15)
    full_name = models.CharField(blank=True, max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    id_number = models.CharField(blank=True, max_length=20, unique=True)
    sex = models.CharField(blank=True, max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    physical_address = models.TextField(blank=True)
    registration_fee_paid = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.membership_no:
            self.membership_no = self.generate_membership_no()
        super().save(*args, **kwargs)

    def generate_membership_no(self):
        now = timezone.now()
        year_prefix = now.strftime('%y')  # e.g., '24' for 2024
        year_prefix = f"{year_prefix}"
        
        # Get the highest current counter for this year
        max_counter = CustomUser.objects.filter(membership_no__startswith=f"CM{year_prefix}").aggregate(
            Max('membership_no')
        )['membership_no__max']
        
        if max_counter:
            # Extract the numeric part of the latest membership_no
            latest_counter = int(max_counter[4:])  # Skip 'CM' and the year prefix
            new_counter = latest_counter + 1
        else:
            # Start from 1 if no previous record exists
            new_counter = 1
        
        # Format the new counter with leading zeros
        counter_str = f"{new_counter:06d}"
        
        return f"CM{year_prefix}{counter_str}"

class Beneficiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    beneficiary_no = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    id_number = models.CharField(blank=True, max_length=20, unique=True)
    sex = models.CharField(blank=True, max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    full_name = models.CharField(blank=True, max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.beneficiary_no:
            self.beneficiary_no = self.generate_beneficiary_no()
        super().save(*args, **kwargs)

    def generate_beneficiary_no(self):
        now = timezone.now()
        year_prefix = now.strftime('%y')  # e.g., '24' for 2024
        
        # Get the highest current counter for this year
        max_counter = Beneficiary.objects.filter(beneficiary_no__startswith=f"BM{year_prefix}").aggregate(
            Max('beneficiary_no')
        )['beneficiary_no__max']
        
        if max_counter:
            # Extract the numeric part of the latest beneficiary_no
            latest_counter = int(max_counter[4:])  # Skip 'BM' and the year prefix
            new_counter = latest_counter + 1
        else:
            # Start from 1 if no previous record exists
            new_counter = 1
        
        # Format the new counter with leading zeros
        counter_str = f"{new_counter:06d}"
        
        return f"BM{year_prefix}{counter_str}"

        
class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_fee_paid = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_ref_no = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    payment_date= models.DateField(auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.payment_ref_no:
            self.payment_ref_no = self.generate_payment_ref_no()
        super().save(*args, **kwargs)

    def generate_payment_ref_no(self):
        now = datetime.now()
        date_part = now.strftime('%y%m%d.%H%M')
        unique_letter = random.choice(string.ascii_uppercase)
        unique_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"S{date_part}.{unique_letter}{unique_part}"

class ShareCapital(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_payments(self):
        return self.sharecapitalpartialpayment_set.aggregate(total=models.Sum('partial_payment'))['total'] or 0

    @property
    def is_fully_paid(self):
        return self.total_payments >= self.amount
class ShareCapitall(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tracks total payments
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Property to check if the user has fully paid the share capital
    @property
    def is_fully_paid(self):
        # Compares the amount paid to the limit defined in settings
        return self.amount >= settings.SHARE_CAPITAL_LIMIT

    # Method to add a payment
    def add_payment(self, payment_amount):
        # Ensure the payment amount is positive
        if payment_amount <= 0:
            raise ValueError("Payment amount must be positive.")
        
        # Calculate the remaining amount needed to reach the capital limit
        required_for_full_payment = settings.SHARE_CAPITAL_LIMIT - self.amount
        
        if payment_amount > required_for_full_payment:
            # If payment exceeds the needed amount, the excess goes to savings
            share_capital_payment = required_for_full_payment  # Amount needed for full payment
            excess_amount = payment_amount - required_for_full_payment  # Remaining amount for savings
        else:
            # If the payment is within the limit, it is applied fully to share capital
            share_capital_payment = payment_amount
            excess_amount = 0  # No excess for savings
        
        # Update the total share capital payment
        self.amount += share_capital_payment
        self.save()
        
        # If there is an excess amount, it is transferred to savings
        if excess_amount > 0:
            # Retrieve or create the Savings object for the user
            savings, created = Savings.objects.get_or_create(user=self.user)
            # Add the excess amount to the user's savings
            savings.add_amount(excess_amount)

    # Override the save method to handle post-save logic
    def save(self, *args, **kwargs):
        # Save the ShareCapitall object first
        super().save(*args, **kwargs)
        
        # Additional actions after saving can be handled here
        if self.is_fully_paid:
            # Optional: Trigger any logic when the share capital is fully paid
            pass

              
class ShareCapitalPartialPayment(models.Model):
    share_capital = models.ForeignKey(ShareCapital, on_delete=models.CASCADE)
    partial_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    partial_payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partial Payment for ShareCapital of ${self.partial_payment} on {self.partial_payment_date}"

class Savings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Savings for {self.user} of ${self.amount}"

class SubscriptionPartialPayment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    partial_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    partial_payment_date = models.DateField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partial Payment for Subscription of ${self.amount} on {self.date}"
    
class LoanTerm(models.Model):
    TERM_CHOICES = [
        (30, '1 Month'),
        (90, '3 Months'),
        (180, '6 Months'),
    ]

    term = models.IntegerField(choices=TERM_CHOICES, unique=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Interest rate as a percentage")

    def __str__(self):
        return f"{self.get_term_display()} - {self.interest_rate}% Interest"

class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Outstanding', 'Outstanding'),
        ('Cleared', 'Cleared'),
    ]
    ref_no = models.CharField(max_length=30, unique=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile_account = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.PositiveIntegerField()  # Duration of the loan in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate as a percentage
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Service fee as a fixed amount
    due_date = models.DateField(blank=True, null=True)
    repayment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    application_date = models.DateField(auto_now_add=True)
    application_time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.ref_no:
            self.ref_no = self.generate_ref_no()
        super().save(*args, **kwargs)

    def generate_ref_no(self):
        now = datetime.now()
        date_part = now.strftime('%y%m%d.%H%M')
        unique_letter = random.choice(string.ascii_uppercase)
        unique_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"CI{date_part}.{unique_letter}{unique_part}"

    def __str__(self):
        return f"{self.full_name} - ${self.amount} for {self.loan_term.get_term_display()}"

class LoanStatus(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='Loan_application_status')
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    total_to_be_repaid = models.DecimalField(max_digits=10, decimal_places=2)
    summary_interest = models.DecimalField(max_digits=10, decimal_places=2)
    overdue_mgt_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    late_interest = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    partial_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    repayment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan Status for Application ID {self.loan_application.id}"