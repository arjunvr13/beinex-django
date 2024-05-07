from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from transaction.functions import calculate_monthly_expense
from .models import Transaction
from user. models import Account, Customer
from .serializers import TransactionSerializer


class MakeTransaction(CreateAPIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        user = request.user
        amount = Decimal(request.data.get('amount'))
        transaction_type = request.data.get('transaction_type')
        to_account_number = request.data.get('to_account_number')  

        if transaction_type not in ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']:
            return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

        if transaction_type in ['WITHDRAWAL', 'TRANSFER']:
            account = Account.objects.get(customer__user=self.request.user)
            account_number = account.account_number
            monthly_expense = calculate_monthly_expense(account_number)
            if account.balance < amount:
                return Response({'error': 'Insufficient Balance'}, status=status.HTTP_400_BAD_REQUEST)
    

            if monthly_expense >= account.expense_limit or monthly_expense+amount >= account.expense_limit:
                return Response({'error': 'Exceeds expense limit. Increase your expense limit to activate transaction'}, status=status.HTTP_400_BAD_REQUEST)
        if transaction_type == 'WITHDRAWAL':
            try:
                customer = user.customer_set.first()  
                account = Account.objects.get(customer=customer)
                expense_limit = account.expense_limit
                

                # if expense_limit < amount:
                #     return Response({'error': 'Exceeds expense limit'}, status=status.HTTP_400_BAD_REQUEST)
                #     # return Response({'warning': 'Exceeds expense limit'}, status=status.HTTP_200_OK)

                # account.expense_limit -= amount
                account.balance -= amount  
                
                transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type)
                transaction.balance = account.balance
                transaction.save()
                account.save()

                return Response({'message': 'Withdrawal successful'}, status=status.HTTP_201_CREATED)

            except Account.DoesNotExist:
                return Response({'error': 'User account not found'}, status=status.HTTP_400_BAD_REQUEST)
        elif transaction_type == 'TRANSFER':
            try:
                from_customer = user.customer_set.first()
                print(from_customer)  
                from_account = Account.objects.get(customer=from_customer)
                to_account = Account.objects.get(account_number=to_account_number)
                print(from_account)
                print(to_account)
                if from_account.balance < amount:
                    return Response({'error': 'Insufficient funds for transfer'}, status=status.HTTP_400_BAD_REQUEST)

                from_account.balance -= amount
                to_account.balance += amount

                transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type,
                                                         from_account_number=from_account.account_number,
                                                         to_account_number=to_account_number)
                transaction.balance = from_account.balance
                transaction.save()

                from_account.save()
                to_account.save()

                return Response({'message': 'Transfer successful'}, status=status.HTTP_201_CREATED)

            except Account.DoesNotExist:
                return Response({'error': 'One of the accounts does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type)
        account = Account.objects.get(customer=user.customer_set.first())
        account.balance += amount
        account.save()

        transaction.balance = account.balance
        transaction.save()
        return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)


    # def post(self, request):
    #     user = request.user
    #     amount = Decimal(request.data.get('amount'))
    #     transaction_type = request.data.get('transaction_type')
    #     to_account_number = request.data.get('to_account_number')  # Assuming to_account_number is provided

    #     if transaction_type not in ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']:
    #         return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Perform internal transfer
    #     if transaction_type == 'TRANSFER':
    #         try:
    #             from_customer = user.customer_set.first()  # Get the Customer associated with the User
    #             from_account = Account.objects.get(customer=from_customer)
    #             to_account = Account.objects.get(account_number=to_account_number)

    #             if from_account.balance < amount:
    #                 return Response({'error': 'Insufficient funds for transfer'}, status=status.HTTP_400_BAD_REQUEST)

    #             from_account.balance -= amount
    #             to_account.balance += amount

    #             transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type, from_account_number=from_account.account_number, to_account_number=to_account_number)
    #             transaction.balance = from_account.balance
    #             transaction.save()

    #             from_account.save()
    #             to_account.save()

    #             return Response({'message': 'transfer successful'}, status=status.HTTP_201_CREATED)

    #         except Account.DoesNotExist:
    #             return Response({'error': 'One of the accounts does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    #     transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type)
    #     account = Account.objects.get(customer=user.customer_set.first())
    #     account.balance += amount
    #     account.save()

    #     transaction.balance = account.balance
    #     transaction.save()
    #     return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)

# class MakeTransaction(CreateAPIView):
#     serializer_class = TransactionSerializer

#     def post(self, request):
#         # if not request.user.is_authenticated:
#         #     return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

#         user = request.user 
#         print(user)
#         amount = Decimal(request.data.get('amount'))
#         transaction_type = request.data.get('transaction_type')

#         if transaction_type not in ['DEPOSIT', 'WITHDRAWAL']:
#             return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

#         if transaction_type == 'WITHDRAWAL':
#             amount = -amount 


#         transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type)

       
#         account = Account.objects.get(customer__user=user)
#         account.balance += amount
#         account.save()
#         transaction.balance = account.balance
#         transaction.save()

#         return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)
    

    

        # def post(self, request):
        # user = request.user 
        # amount = request.data.get('amount')
        # transaction_type = request.data.get('transaction_type')
        # to_account_number = request.data.get('to_account_number')

        # if not amount or not transaction_type:
        #     return Response({'error': 'Amount and transaction type are required'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     amount = Decimal(amount)
        # except Decimal.InvalidOperation:
        #     return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        # if transaction_type not in ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']:
        #     return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

        # if transaction_type == 'WITHDRAWAL':
        #     amount = -amount 

        # if transaction_type == 'TRANSFER':
        #     if not to_account_number:
        #         return Response({'error': 'Destination account number is required for transfer'}, status=status.HTTP_400_BAD_REQUEST)
            
        #     try:
        #         to_account = Account.objects.get(account_number=to_account_number)
        #     except Account.DoesNotExist:
        #         return Response({'error': 'Destination account not found'}, status=status.HTTP_400_BAD_REQUEST)

        #     if user.account.balance < amount:
        #         return Response({'error': 'Insufficient funds for transfer'}, status=status.HTTP_400_BAD_REQUEST)

        #     user.account.balance -= amount
        #     to_account.balance += amount
        #     user.account.save()
        #     to_account.save()

        # transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=transaction_type)
        # transaction.balance = user.account.balance
        # transaction.save()

        # return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)
