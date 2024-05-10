from django.db import models
from user.models import User

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_progress = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

