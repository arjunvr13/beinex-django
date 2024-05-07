# serializer.py
from datetime import datetime
from decimal import Decimal
from rest_framework import serializers
from .models import LoanApplication
from .constants import (
    PERSONAL_LOAN_INTEREST_RATE,
    HOME_LOAN_INTEREST_RATE,
    CAR_LOAN_INTEREST_RATE,
    EDUCATION_LOAN_INTEREST_RATE,
)

class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = ['id', 'loan_type', 'amount', 'tenure_months', 'interest_rate', 'applied_date', 'status', 'approved_date']
        
    def validate_loan_type(self, value):
        valid_loan_types = ['PERSONAL_LOAN', 'HOME_LOAN', 'CAR_LOAN', 'EDUCATION_LOAN']
        if value not in valid_loan_types:
            raise serializers.ValidationError("Invalid loan type")
        return value
    
    def validate(self, data):
        loan_type = data.get('loan_type')
        if loan_type == 'PERSONAL_LOAN':
            data['interest_rate'] = PERSONAL_LOAN_INTEREST_RATE
        elif loan_type == 'HOME_LOAN':
            data['interest_rate'] = HOME_LOAN_INTEREST_RATE
        elif loan_type == 'CAR_LOAN':
            data['interest_rate'] = CAR_LOAN_INTEREST_RATE
        elif loan_type == 'EDUCATION_LOAN':
            data['interest_rate'] = EDUCATION_LOAN_INTEREST_RATE
        else:
            raise serializers.ValidationError("Invalid loan type")

        return data
    
    def validate_status(self, value):
        valid_statuses = ['pending', 'approved', 'rejected']
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status")
        return value
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if instance.status == 'approved' and instance.approved_date is None:
            instance.approved_date = datetime.now()
        instance.save()
        return instance
    
def get_interest_rate(loan_type):
    if loan_type == 'PERSONAL_LOAN':
        return Decimal(str(PERSONAL_LOAN_INTEREST_RATE))  
    elif loan_type == 'HOME_LOAN':
        return Decimal(str(HOME_LOAN_INTEREST_RATE))  
    elif loan_type == 'CAR_LOAN':
        return Decimal(str(CAR_LOAN_INTEREST_RATE))  
    elif loan_type == 'EDUCATION_LOAN':
        return Decimal(str(EDUCATION_LOAN_INTEREST_RATE))  
    else:
        raise serializers.ValidationError("Invalid loan type")
    
class LoanAmountSerializer(serializers.Serializer):
    principal_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1)
    loan_type = serializers.ChoiceField(choices=['PERSONAL_LOAN', 'HOME_LOAN', 'CAR_LOAN', 'EDUCATION_LOAN'])

    def validate_loan_type(self, value):
        interest_rate = get_interest_rate(value)
        self.context['interest_rate'] = interest_rate  
        return value

    def calculate_total_payable_amount(self, validated_data):
        principal_amount = validated_data['principal_amount']
        tenure_months = validated_data['tenure_months']
        interest_rate = self.context['interest_rate'] / 100  
        monthly_interest_rate = interest_rate / 12
        total_amount = principal_amount + (principal_amount * monthly_interest_rate * tenure_months)
        monthly_payable_amount = total_amount / tenure_months
        return {'total_amount': total_amount, 'monthly_payable_amount': monthly_payable_amount,'tenure_months':tenure_months}