from django.urls import path, include
from .views import *


urlpatterns = [
    path('create-fixed-deposit/', CreateFixedDeposit.as_view(), name='create_fixed_deposit'),
    path('list-fixed-deposits/', ListUserFixedDeposits.as_view(), name='list_user_fixed_deposits'),
    path('deposit-calculator/', DepositCalculator.as_view(), name='deposit_calculator'),
    path('deposit-check/<int:id>', FixedDepositBalanceCheck.as_view(), name='deposit_check'),
    path('create-recurring-deposit/', CreateRecurringDeposit.as_view(), name='create_recurring_deposit'),
    path('list-recurring-deposits/', ListUserRecurringDeposits.as_view(), name='list_user_recurring_deposits'),
    path('deposit-calculator-recurring/', RecurringDepositCalculator.as_view(), name='deposit_calculator_recurring'),
    path('recurring-deposit-check/<int:id>', RecurringDepositBalanceCheck.as_view(), name='recurring_deposit_check'),
]
