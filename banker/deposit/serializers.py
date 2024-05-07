from datetime import datetime
from decimal import Decimal
from rest_framework import serializers
from .models import FixedDeposit, FIXED_INTEREST_RATE, RecurringDeposit, RECURRING_DEPOSIT_RATE
from datetime import date


class FixedDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedDeposit
        fields = ['principal_amount','tenure_months']

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance
    

class FixedDepositAmountSerializer(serializers.Serializer):
    principal_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1)

    def validate_tenure_months(self, value):
        if value % 12 != 0:
            raise serializers.ValidationError("Tenure should be in months.")
        return value

    def calculate_total_amount(self, validated_data):
        principal_amount = validated_data['principal_amount']
        tenure_months = validated_data['tenure_months']
        monthly_interest_rate = Decimal(str(FIXED_INTEREST_RATE)) / 12 / 100
        total_amount = principal_amount + (principal_amount * monthly_interest_rate * tenure_months)
        return total_amount
    


class FixedDepositBalanceCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedDeposit
        fields = '__all__'

    current_amount = serializers.SerializerMethodField()
    def get_current_amount(self, obj):        
        principal_amount = obj.principal_amount
        tenure_months = obj.tenure_months
        start_date = obj.start_date
        current_date = date.today() 
        print(current_date.year)
        elapsed_months = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
        monthly_interest_rate = Decimal(str(FIXED_INTEREST_RATE)) / 12 / 100
        current_amount = principal_amount + (principal_amount * monthly_interest_rate * elapsed_months)

        return current_amount



class RecurringDepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecurringDeposit
        fields = ['principal_amount','tenure_months']

    def create(self, validated_data):
        instance = super().create(validated_data)
        # instance.calculate_maturity_amount()
        return instance
    
class RecurringDepositCalculatorSerializer(serializers.Serializer):
    principal_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1)

    def validate_tenure_months(self, value):
        if value % 12 != 0:
            raise serializers.ValidationError("Tenure should be in multiples of 12 (months).")
        return value

    def calculate_total_amount(self, validated_data):
        principal_amount = validated_data['principal_amount']
        tenure_months = validated_data['tenure_months']
        monthly_interest_rate = Decimal(str(RECURRING_DEPOSIT_RATE)) / 12 / 100

        total_amount = Decimal('0')
        current_amount = Decimal(principal_amount)
        for month in range(tenure_months):
            current_amount += current_amount * monthly_interest_rate
            total_amount += current_amount

        return total_amount


class RecurringDepositBalanceCheckSerializer(serializers.ModelSerializer):
    current_amount = serializers.SerializerMethodField()

    class Meta:
        model = RecurringDeposit
        fields = ['principal_amount', 'tenure_months', 'start_date', 'current_amount']

    def get_current_amount(self, obj):
        principal_amount = obj.principal_amount
        tenure_months = obj.tenure_months
        start_date = obj.start_date
        current_date = date.today()
        # current_date_str = '2025-05-03'
        # current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
        print(current_date)

        elapsed_months = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
        monthly_interest_rate = Decimal(str(RECURRING_DEPOSIT_RATE)) / 12 / 100

        total_amount = Decimal('0')
        current_amount = Decimal(principal_amount)
        for month in range(elapsed_months):
            current_amount += current_amount * monthly_interest_rate
            total_amount += current_amount

        return total_amount