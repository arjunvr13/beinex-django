from django.urls import path, include
from. views import *

urlpatterns = [
    path('create_customer/',CustomerDetail.as_view(),name='create_customer'),
    path('list_customer/',ViewCustomerDetails.as_view(),name='list_customer'),
    path('login/', Login.as_view(), name='login'),
    path('customer-dash/', CustomerDash.as_view(), name='customer_dash'),
    path('account-statement/', ViewAccountStatement.as_view(), name='account_statement'),
    path('view-balance/', ViewBalance.as_view(), name='view_balance'),
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    path('set-expense-limit/', ExpenseLimitView.as_view(), name='set_expense_limit'),
]
