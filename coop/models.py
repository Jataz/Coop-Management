from datetime import datetime, timedelta
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
        # Only generate a membership number if it does not exist
        if not self.membership_no:
            with transaction.atomic():
                # Lock the table to prevent race conditions
                last_member = CustomUser.objects.select_for_update().aggregate(Max('membership_no'))
                last_number = last_member['membership_no__max']

                if last_number:
                    # Extract the last number and increment it
                    match = re.match(r'CM(\d+)', last_number)
                    if match:
                        next_number = int(match.group(1)) + 1
                    else:
                        next_number = 1
                else:
                    next_number = 1

                # Generate the new membership number
                self.membership_no = f"CM{next_number}"

        super().save(*args, **kwargs)

class Beneficiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    beneficiary_no = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    id_number = models.CharField(blank=True, max_length=20, unique=True)
    sex = models.CharField(blank=True, max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    full_name = models.CharField(blank=True, max_length=255)
    
    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.beneficiary_no:
            with transaction.atomic():
                # Lock the table to prevent race conditions
                last_beneficiary = Beneficiary.objects.select_for_update().aggregate(Max('beneficiary_no'))
                last_number = last_beneficiary['beneficiary_no__max']

                if last_number:
                    # Extract the last number and increment it
                    match = re.match(r'BN(\d+)', last_number)
                    if match:
                        next_number = int(match.group(1)) + 1
                    else:
                        next_number = 1
                else:
                    next_number = 1

                # Generate the new beneficiary number
                self.beneficiary_no = f"BN{next_number}"

        super().save(*args, **kwargs)
        
class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_fee_paid = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    payment_date= models.DateField(auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShareCapital(models.Model):
    user = user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubscriptionPartialPayment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    partial_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    partial_payment_date = models.DateField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partial Payment for Subscription of ${self.amount} on {self.date}"

class ShareCapitalPartialPayment(models.Model):
    share_capital = models.ForeignKey(ShareCapital, on_delete=models.CASCADE)
    partial_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    partial_payment_date = models.DateField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partial Payment for ShareCapital of ${self.amount} on {self.date}"
    
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