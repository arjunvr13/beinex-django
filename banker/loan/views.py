from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .constants import (
    PERSONAL_LOAN_INTEREST_RATE,
    HOME_LOAN_INTEREST_RATE,
    CAR_LOAN_INTEREST_RATE,
    EDUCATION_LOAN_INTEREST_RATE,
)
from .serializers import LoanApplicationSerializer, LoanAmountSerializer
from .models import LoanApplication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class LoanApplicationCreateView(generics.CreateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        loan_type = serializer.validated_data.get('loan_type')
        amount = serializer.validated_data.get('amount')
        tenure_months = serializer.validated_data.get('tenure_months')

        interest_rate = None
        if loan_type == 'PERSONAL_LOAN':
            interest_rate = PERSONAL_LOAN_INTEREST_RATE
        elif loan_type == 'HOME_LOAN':
            interest_rate = HOME_LOAN_INTEREST_RATE
        elif loan_type == 'CAR_LOAN':
            interest_rate = CAR_LOAN_INTEREST_RATE
        elif loan_type == 'EDUCATION_LOAN':
            interest_rate = EDUCATION_LOAN_INTEREST_RATE
        else:
            raise serializer.ValidationError("Invalid loan type")
        
        serializer.save(interest_rate=interest_rate, user=self.request.user, status='pending')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if interest_rate is not None:
        #     serializer.save(interest_rate=interest_rate, user=self.request.user, status='pending')
        # else:
        #     raise serializer.ValidationError("Interest rate not specified for loan type")

        # return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoanApplicationUpdateView(generics.UpdateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]


    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('loan.change_loanapplication'):
            return Response({"message": "User does not have the required permission"}, status=status.HTTP_200_OK)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'status' in request.data:
            instance.status = request.data['status']
        if 'approved_date' in request.data:
            instance.approved_date = request.data['approved_date']
        updated_instance = serializer.save()
        return Response(self.get_serializer(updated_instance).data, status=status.HTTP_200_OK)
    
class LoanCalculator(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanAmountSerializer(data=request.data)
        if serializer.is_valid():
            total_payable_amount = serializer.calculate_total_payable_amount(serializer.validated_data)
            return Response({'total_payable_amount': total_payable_amount}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)