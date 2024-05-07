from django.urls import path, include
from. views import *

urlpatterns = [
    path('apply-loan/', LoanApplicationCreateView.as_view(), name='apply_loan'),
    path('update-loan/<int:pk>', LoanApplicationUpdateView.as_view(), name='update_loan'),
    path('loan-calculator/', LoanCalculator.as_view(), name='loan_calculator'),

]
