from datetime import datetime
from django.db.models import Q, Sum
from transaction.models import Transaction

def calculate_monthly_expense(self_account_number):
    total_expense = 0
    current_month = datetime.now().month
    transactions = Transaction.objects.filter(
        # Q(transaction_type="WITHDRAWAL") | Q(transaction_type="TRANSFER"),
        timestamp__month=current_month,
    )

    # total_expense = transactions.aggregate(total=Sum('amount'))['total'] or 0
    for transaction in transactions:
        if transaction.transaction_type == 'WITHDRAWAL':
            total_expense = total_expense+transaction.amount
        elif transaction.transaction_type == 'TRANSFER':
            if transaction.from_account_number == self_account_number:
                total_expense = total_expense+transaction.amount
    print(total_expense)
    return total_expense