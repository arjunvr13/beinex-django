from django.db import models
from user. models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'DEPOSIT'),
        ('WITHDRAWAL', 'WITHDRAWAL'),
        ('TRANSFER', 'TRANSFER'),
    )
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    from_account_number = models.CharField(max_length=20, blank=True, null=True)  # Account number transferring from
    to_account_number = models.CharField(max_length=20, blank=True, null=True)    # Account number transferring to

    def save(self, *args, **kwargs):
        if self.transaction_type != 'TRANSFER':
            self.from_account_number = None
            self.to_account_number = None
        super().save(*args, **kwargs)