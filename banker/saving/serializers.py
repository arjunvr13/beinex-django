from rest_framework import serializers
from .models import SavingGoal

class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = ['id', 'goal_amount', 'current_progress', 'created_at']
