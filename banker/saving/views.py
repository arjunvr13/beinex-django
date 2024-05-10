from decimal import Decimal
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import SavingGoal
from user.models import Account
from .serializers import SavingGoalSerializer

class CreateSavingGoal(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavingGoalSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListSavingGoals(ListAPIView):
    serializer_class = SavingGoalSerializer

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)


class UpdateSavingGoalProgress(APIView):
    def post(self, request, *args, **kwargs):
        goal_id = kwargs.get('goal_id')
        desired_amount = Decimal(request.data.get('desired_amount'))
        goal = get_object_or_404(SavingGoal, id=goal_id, user=request.user)
        
        account = get_object_or_404(Account, customer__user=request.user)
        current_balance = account.balance
        # print(current_balance)

        if desired_amount > current_balance:
            return Response({'error': 'Insufficient balance in your account'}, status=status.HTTP_400_BAD_REQUEST)

        account.balance -= desired_amount
        account.save()

        goal.current_progress += desired_amount
        goal.save()

        serializer = SavingGoalSerializer(goal)
        return Response(serializer.data)


# class UpdateSavingGoalProgress(APIView):
#     def post(self, request, *args, **kwargs):
#         goal_id = kwargs.get('goal_id')
#         try:
#             goal = SavingGoal.objects.get(id=goal_id, user=request.user)
#             desired_amount = Decimal(request.data.get('desired_amount'))
#             goal.current_progress += desired_amount
#             goal.save()
#             serializer = SavingGoalSerializer(goal)
#             return Response(serializer.data)
#         except SavingGoal.DoesNotExist:
#             return Response({'error': 'Saving goal not found'}, status=status.HTTP_404_NOT_FOUND)
