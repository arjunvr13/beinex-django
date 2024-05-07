from django.db import models
from user. models import User
from .constants import (
    FIXED_INTEREST_RATE,
    RECURRING_DEPOSIT_RATE
)

class FixedDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    start_date = models.DateField(auto_now_add=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=FIXED_INTEREST_RATE)


class RecurringDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    start_date = models.DateField(auto_now_add=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=RECURRING_DEPOSIT_RATE)
