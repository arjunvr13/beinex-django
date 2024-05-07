from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_regex_validator = RegexValidator(
        regex = r'^\d{10}$',
        message = 'phone number must be 10 digits'
    )
    mobile_number = models.CharField(
        max_length=10,
        validators=[mobile_regex_validator],
        unique=True,
        blank=False,
        null=False
        )
    aadhar_regex_validator = RegexValidator(
        regex=r'^\d{12}$',
        message='Aadhar number must be 12 digits'
    )
    aadhar_number = models.CharField(
        max_length=12,
        validators=[aadhar_regex_validator],
        unique=True,
        blank=False,
        null=False       
    )    
    user_id= models.AutoField(primary_key=True)




class Customer(models.Model):
    pan_regex_validator = RegexValidator(
        regex = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
        message = 'Enter the pan in correct format'
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pan_number = models.CharField(
        max_length=10,
        validators=[pan_regex_validator],
        unique=True,
        blank=False,
        null=False
    )

class Account(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    ACCOUNT_CHOICES = (
        ('SAVING','SAVING'),
        ('CURRENT','CURRENT')
    )
    account_type = models.CharField(choices=ACCOUNT_CHOICES, max_length=20)
    account_number = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    expense_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)


