from django.core.validators import RegexValidator, MinLengthValidator

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^(0)\d{9}$', message="Phone number must be entered in the format: '0540123466'.")
    min_length = MinLengthValidator(10, message="Phone number should be 10 digits")
    phone = models.CharField(validators=[phone_regex, min_length], max_length=10) 
    wallet = models.IntegerField(default=0)
    address = models.CharField(max_length=500)
    referrer = models.CharField(max_length=100, default="No referrer")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
