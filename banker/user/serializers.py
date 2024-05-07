from rest_framework import serializers
from . models import User, Customer, Account 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from datetime import datetime
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class CreateCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=10)
    aadhar_number = serializers.CharField(max_length=12)
    pan_number = serializers.CharField(max_length=12)
    account_type = serializers.CharField(max_length=12)
    date_of_birth = serializers.CharField(max_length=12)
  


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'username',
            'mobile_number',
            'aadhar_number',
            'date_of_birth'
        ]
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['user', 'account_type', 'account_number']
        read_only_fields = ['account_number']

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(style={"input_type":"password"})

    class Meta:
        model = User  
        fields = ['username', 'password']

class LoginResponseSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    def get_refresh_token(self, instance):
        return str(RefreshToken.for_user(instance))
    
    def get_access_token(self, instance):
        return str(RefreshToken.for_user(instance).access_token)
    
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "access_token",
            "refresh_token"
        ]


class CustomerDashSerializer(serializers.ModelSerializer):
    account_type = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()
    last_transactions = serializers.SerializerMethodField()
    expense_limit = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','account_number', 'date_of_birth', 'account_type','expense_limit', 'last_transactions']

    def get_account_type(self, user):
        try:
            account = Account.objects.get(customer__user=user)
            return account.account_type
        except Account.DoesNotExist:
            return None

    def get_account_number(self, user):
        try:
            account = Account.objects.get(customer__user=user)
            return account.account_number
        except Account.DoesNotExist:
            return None
        
    
    def get_last_transactions(self, user):
        try:
            transactions = Transaction.objects.filter(user=user).order_by('-timestamp')[:5]
            serializer = TransactionSerializer(transactions, many=True)
            return serializer.data
        except Transaction.DoesNotExist:
            return None
        
    def get_expense_limit(self, user):
        account = Account.objects.get(customer__user=user)
        return account.expense_limit
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        transactions = data.get('last_transactions', [])
        for transaction in transactions:
            transaction_type = transaction.get('transaction_type', '')
            if transaction_type in ['WITHDRAWAL', 'DEPOSIT']:
                transaction.pop('from_account_number', None)
                transaction.pop('to_account_number', None)
        return data
        
    
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # Check if the old password matches the user's current password
        if not check_password(data.get('old_password'), user.password):
            raise serializers.ValidationError("Current password is incorrect.")

        # Check if new password and confirm new password match
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError("New passwords do not match.")

        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class ViewBalanceSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['balance', 'account_number']

    def get_balance(self, user):
        account = Account.objects.get(customer__user=user)
        return account.balance
        
        
    def get_account_number(self, user):
        account = Account.objects.get(customer__user=user)
        return account.account_number
    
class ExpenseLimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['expense_limit']

