from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=255 )
    date_of_birth = models.DateField()
    id_number = models.CharField(max_length=20, unique=True )
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')] )
    physical_address = models.TextField()
    
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