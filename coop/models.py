from datetime import datetime, timedelta
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(blank=True,max_length=15)
    full_name = models.CharField(blank=True,max_length=255 )
    date_of_birth = models.DateField(null=True,blank=True)
    id_number = models.CharField(blank=True,max_length=20, unique=True )
    sex = models.CharField(blank=True,max_length=1, choices=[('M', 'Male'), ('F', 'Female')] )
    physical_address = models.TextField(blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email
    

class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_fee_paid = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    
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
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('outstanding', 'Outstanding'),
        ('cleared', 'Cleared'),
    ]
        
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile_account = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.PositiveIntegerField()  # Duration of the loan in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))  # Interest rate as a percentage
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('2.00'))  # Service fee as a fixed amount
    due_date = models.DateField(blank=True, null=True)
    repayment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    application_date = models.DateField(auto_now_add=True)
    application_time = models.TimeField(auto_now_add=True)
    agreed_to_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

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

    def __str__(self):
        return f"Loan Status for Application ID {self.loan_application.id}"