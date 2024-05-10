from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-saving-goal/', CreateSavingGoal.as_view(), name='create_saving_goal'),
    path('list-saving-goals/', ListSavingGoals.as_view(), name='list_saving_goals'),
    path('update-saving-goal/<int:goal_id>', UpdateSavingGoalProgress.as_view(), name='update_saving_goal_progress'),
]
