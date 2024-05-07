from django.db import models
from user. models import User
from .constants import (
    PERSONAL_LOAN_INTEREST_RATE,
    HOME_LOAN_INTEREST_RATE,
    CAR_LOAN_INTEREST_RATE,
    EDUCATION_LOAN_INTEREST_RATE,
)
LOAN_TYPES = (
    ('PERSONAL_LOAN', 'PERSONAL_LOAN'),
    ('HOME_LOAN', 'HOME_LOAN'),
    ('CAR_LOAN', 'CAR_LOAN'),
    ('EDUCATION_LOAN', 'EDUCATION_LOAN'),
)

class LoanApplication(models.Model):
    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=100, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=PERSONAL_LOAN_INTEREST_RATE,
    )
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
