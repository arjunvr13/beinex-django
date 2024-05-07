from datetime import date
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import FixedDeposit, RecurringDeposit
from rest_framework.views import APIView
from .serializers import FixedDepositSerializer, FixedDepositAmountSerializer, FixedDepositBalanceCheckSerializer, RecurringDepositSerializer, RecurringDepositCalculatorSerializer, RecurringDepositBalanceCheckSerializer
from .constants import (
    FIXED_INTEREST_RATE,
    RECURRING_DEPOSIT_RATE
)

#fixed deposit
class CreateFixedDeposit(CreateAPIView):
    queryset = FixedDeposit.objects.all()
    serializer_class = FixedDepositSerializer

    def perform_create(self, serializer):
        interest_rate = FIXED_INTEREST_RATE
        serializer.save(user=self.request.user, interest_rate=interest_rate)

class ListUserFixedDeposits(ListAPIView):
    serializer_class = FixedDepositSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FixedDeposit.objects.filter(user=self.request.user)


class DepositCalculator(ListAPIView):
    serializer_class = FixedDepositAmountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FixedDepositAmountSerializer(data=request.data)
        if serializer.is_valid():
            total_amount = serializer.calculate_total_amount(serializer.validated_data)
            return Response({'total_amount': total_amount}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FixedDepositBalanceCheck(APIView):
    
    def get(self, request, id):
        try:
            instance = FixedDeposit.objects.get(id=id)
            print(instance)
            serializer = FixedDepositBalanceCheckSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FixedDeposit.DoesNotExist:
            return Response({"message": "Fixed deposit not found"}, status=status.HTTP_404_NOT_FOUND)
        

#recurring deposit
class CreateRecurringDeposit(CreateAPIView):
    queryset = RecurringDeposit.objects.all()
    serializer_class = RecurringDepositSerializer

    def perform_create(self, serializer):
        interest_rate = RECURRING_DEPOSIT_RATE
        serializer.save(user=self.request.user, interest_rate=interest_rate)


class ListUserRecurringDeposits(ListAPIView):
    serializer_class = RecurringDepositSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecurringDeposit.objects.filter(user=self.request.user)
    

class RecurringDepositCalculator(APIView):
    def post(self, request, format=None):
        serializer = RecurringDepositCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            total_amount = serializer.calculate_total_amount(serializer.validated_data)
            return Response({'total_amount': total_amount}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RecurringDepositBalanceCheck(APIView):
    
    def get(self, request, id):
        try:
            instance = RecurringDeposit.objects.get(id=id)
            print(instance)
            serializer = RecurringDepositBalanceCheckSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RecurringDeposit.DoesNotExist:
            return Response({"message": "Fixed deposit not found"}, status=status.HTTP_404_NOT_FOUND)