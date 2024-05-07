from typing import OrderedDict
from rest_framework import status
from django.contrib.auth import authenticate, login
import time
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .pagination import CustomPagination
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView
from . serializers import ChangePasswordSerializer, UserSerializer, CreateCustomerSerializer, LoginSerializer, LoginResponseSerializer, CustomerDashSerializer, ViewBalanceSerializer, ExpenseLimitSerializer
from . models import User, Customer, Account
from transaction.serializers import TransactionSerializer, ViewStatementSerializer
from transaction.models import Transaction


class CustomerDetail(CreateAPIView):
    # serializer_class = UserSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('user.add_account'):
            return Response({"message": "User does not have the required permission"}, status=status.HTTP_200_OK)
        serializer = CreateCustomerSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(Q(username=serializer.validated_data['username'])|Q(aadhar_number=serializer.validated_data['aadhar_number'])).exists():
                return Response({"error": "User with same username or aadhar number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if Customer.objects.filter(pan_number=serializer.validated_data['pan_number']).exists():
                return Response({"error": "User with same pan number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            first_name = serializer.validated_data['first_name']
            password = first_name.lower()
            hashed_password = make_password(password)

            user_obj = User.objects.create(
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                username = serializer.validated_data['username'],
                mobile_number = serializer.validated_data['mobile_number'],
                aadhar_number = serializer.validated_data['aadhar_number'],
                date_of_birth = serializer.validated_data['date_of_birth'],
                password = hashed_password
            )
            try:
                group_obj = Group.objects.get(name='customer') 
            except:
                return Response({"error": "Customer group does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            user_obj.groups.add(group_obj)

            customer_obj = Customer.objects.create(
                user = user_obj,
                pan_number = serializer.validated_data['pan_number'],
            )

            account_number = f"{int(time.time())}{user_obj.user_id}"

            account_obj = Account.objects.create(
                customer = customer_obj,
                account_type = serializer.validated_data['account_type'],
                account_number = account_number
            )

            subject = 'Welcome to Our Bank!'
            message = f'Dear {user_obj.first_name},\n\nWelcome to Our Bank! Your account has been successfully created.'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [user_obj.username]  
            send_mail(subject, message, from_email, recipient_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # def post(self, request, *args, **kwargs):
    #     user_serializer = UserSerializer(data=request.data)
    #     if user_serializer.is_valid():
    #         user_instance = user_serializer.save()

    #         account_number = f"{int(time.time())}{user_instance.id}"
    #         print(account_number)
    #         return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   


class ViewCustomerDetails(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('user.view_account'):
            return Response({"message": "User does not have the required permission"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
    


class Login(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user_obj = User.objects.get(username__iexact=data["username"])
                print(user_obj.password)
                print(data['password'])
                if (data['password'], user_obj.password):
                    user_obj.last_login = timezone.now()
                    print("hellow")
                    user_obj.save()

                    resp = LoginResponseSerializer(instance=user_obj)
                    return Response(resp.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Invalid credentials", "status": "1"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response({"message": "Invalid user", "status": "1"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         # Update last login time
        #         login(request, user)
        #         # user.last_login = timezone.now()
        #         # user.save()
        #         return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerDash(RetrieveAPIView):
    serializer_class = CustomerDashSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ViewBalance(RetrieveAPIView):
    serializer_class = ViewBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ViewAccountStatement(ListAPIView):
    serializer_class = ViewStatementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

  
    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user).order_by('-timestamp')
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ViewStatementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ViewStatementSerializer(queryset, many=True)
        return Response(serializer.data)
    

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExpenseLimitView(APIView):
    serializer_class = ExpenseLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        account = Account.objects.filter(customer__user=user).first()
        return account

    def get(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.serializer_class(account)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.serializer_class(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)